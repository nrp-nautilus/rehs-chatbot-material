# Requesting FPGAs and JTAG from a Pod

Source: https://nrp.ai/documentation/userdocs/fpgas/using-fpgas-from-pods

# Requesting FPGAs and JTAG from a Pod

This page covers raw-Kubernetes usage. If you want a turnkey environment with Vivado/Vitis pre-installed, see AMD/Xilinx FPGAs in Coder — it spins up a pod from a template that already has the right resource requests.

## Which workflow do you want?

There are three common ways to get an FPGA on NRP. Pick the one that matches what you’re trying to do:

Rule of thumb on Coder vs. your own pod:

- Use Coder when you want a one-click developer environment with all the tools, GUI, and license env already wired up — and you’re going to be interactive.

- Use your own pod/Job when you want to run unattended (CI, overnight synthesis), need a different image or different Vivado/Vitis version, or want full control over the spec (e.g. pinning to a specific card by iSerial).

The two are not exclusive — many users develop in Coder and submit long batch jobs from their namespace using the same image.

## Frequently asked questions

Quick answers to the questions that come up most often. Each one links to the longer treatment further down the page.

Q: I just want to load my .xclbin and run my host app — what’s the minimum? A: A pod requesting amd.com/xilinx_u55c_gen3x16_xdma_base_3-0: 1 and an image that has XRT (e.g. the Coder vivado-vitis image). You do not need xilinx.com/fpga_jtag . See XRT in your pod .

Q: Do I need to request xilinx.com/fpga_jtag ? A: Almost certainly no. JTAG is only needed for reflashing the base shell, attaching Vivado hw_server / xsdb / OpenOCD, or reading the SC over UART. Loading kernels, running Vitis-built designs, and running ESnet SmartNIC pipelines all use the AMD card resource above. See Before you request JTAG .

Q: How do I launch Vivado / Vitis in a Coder workspace? A: In the u55c-xilinx Coder template, just open the XFCE or code-server terminal and type vivado (or vitis , vlm ). The license server env and settings64.sh are sourced automatically. See Using Vivado/Vitis with the cluster license server .

Q: How do I tell which physical Alveo card I got allocated? A: Inside the pod, the FTDI iSerial of the JTAG cable equals the card’s XMC serial. Read it from sysfs — see Example 3 .

Q: Where is the license server? A: [email protected] (cluster-internal DNS). Already set as XILINXD_LICENSE_FILE in the Coder template; otherwise export [email protected] .

Q: Vivado crashes inside the container with a realloc() / corrupted size error. A: Known issue. Try the LD_LIBRARY_PATH workaround . If that doesn’t work, run Vivado inside a KubeVirt VM instead.

Q: My pod stays in Pending with “Insufficient amd.com/xilinx_u55c_* ”. A: All FPGAs that can satisfy your request are currently allocated to other workloads, or you asked for more cards than any single host has. See troubleshooting .

Q: Can I just flash a card myself? A: No — flashing requires a chassis power cycle that evicts everybody on the node. Contact cluster admins on Nautilus Support to coordinate a window. See Flashing a card’s base shell from a pod .

Q: Which Vivado/Vitis versions are installed? A: Vivado 2021.2, 2023.1, 2023.2 ; Vitis 2021.2, 2023.2 (no Vitis 2023.1). All under /tools/Xilinx/ . Switch versions in the Coder template’s Vivado / Vitis version parameter, or source /tools/Xilinx/Vivado/<ver>/settings64.sh by hand.

## Before you request JTAG: read this

## The resources you can request

Two independent device plugins surface FPGA hardware to Kubernetes. The resource names you’ll put under resources.limits :

Counts per host (current as of 2026-06-03):

## The pairing problem (and the clean way to solve it)

The AMD plugin (FPGA) and KubeVirt’s USB plugin (JTAG) don’t talk to each other. On a 2-card host, asking for 1 of each can give you card A and JTAG cable B .

Useful fact verified by experiment: /sys/bus/usb/devices/ and /sys/bus/pci/devices/ are visible to every container regardless of which resource you requested. That means lsusb -v inside the pod can read the iSerial of every FTDI FT4232H on the host, and the Alveo XMC serial under /sys/... is readable too. The FTDI iSerial is identical to the card’s XMC serial number — Xilinx programs both with the same string. So you can always tell at runtime which JTAG cable corresponds to which FPGA.

That makes the practical recipe:

- Request what you need (1 FPGA + 1 JTAG, or N of each, or all on the host).

- Inside the pod, look up the iSerial of the JTAG cable(s) you actually got by reading /sys/bus/usb/devices/<N-N>/serial for the FTDI device(s) that match /dev/bus/usb/<bus>/<dev> .

- Match against the FPGA BDF’s XMC serial read from xbutil examine or /sys/bus/pci/drivers/xclmgmt/<BDF>/xmc.*/serial_num .

- If they match, you’re good. If they don’t, either request all of them so all pairs land in your pod, or pin to a single-card host where there’s only one possible pair.

### Patterns

- Take the whole host. Request every FPGA and every JTAG on the host. Every JTAG is then for one of your FPGAs — no mismatch possible. Use the iSerial match in code to pair them up.

- Pin to a single-card host ( node-2-9 or node-2-10 ). There’s only one FPGA and one JTAG, so the allocation is the matching pair by construction.

- Pin to a specific card by hostname + serial check. Use nodeSelector to land on the host that has the card you want, request 1 + 1 , then check the iSerial inside the pod and exit (or restart) if it isn’t your target.

## Example 1 — single FPGA + JTAG on a 1-card host (guaranteed pair)

```
apiVersion: v1
kind: Pod
metadata:
  name: fpga-single
  namespace: my-namespace
spec:
  restartPolicy: Never
  nodeSelector:
    kubernetes.io/hostname: node-2-9.sdsc.optiputer.net   # 1 card, 1 JTAG → matched
  containers:
  - name: dev
    image: ubuntu:22.04
    command: ["sleep", "infinity"]
    resources:
      limits:
        amd.com/xilinx_u55c_gen3x16_xdma_base_3-0: 1
        xilinx.com/fpga_jtag:                    1
        memory: 8Gi
        cpu: "2"
      requests:
        memory: 8Gi
        cpu: "2"
```

## Example 2 — take the whole multi-card host

```
apiVersion: v1
kind: Pod
metadata:
  name: fpga-dev
  namespace: my-namespace
spec:
  restartPolicy: Never
  nodeSelector:
    kubernetes.io/hostname: node-2-7.sdsc.optiputer.net   # 2 cards on this host
  containers:
  - name: dev
    image: ubuntu:22.04
    command: ["sleep", "infinity"]
    resources:
      limits:
        amd.com/xilinx_u55c_gen3x16_xdma_base_3-0: 2   # both cards
        xilinx.com/fpga_jtag:                    2   # both JTAGs
        memory: 16Gi
        cpu: "4"
      requests:
        memory: 16Gi
        cpu: "4"
```

/dev/bus/usb/... will contain exactly the two FT4232H device files; their iSerials will be the two card serials.

## Example 3 — verify the pairing at runtime

Drop this into any of the pod images above (with usbutils installed). It walks /dev/bus/usb/ , reads each device’s iSerial via /sys , and prints the BDF↔serial pairing it observes:

```
apt-get update -qq && apt-get install -yqq usbutils >/dev/null

echo "JTAG cables passed into this pod:"
for f in /dev/bus/usb/*/* ; do
    bus=$(basename "$(dirname "$f")")
    dev=$(basename "$f")
    bus_dec=$((10#$bus)); dev_dec=$((10#$dev))
    for sd in /sys/bus/usb/devices/*/; do
        [ -f "${sd}busnum" ] || continue
        if [ "$(cat "${sd}busnum")" = "$bus_dec" ] && [ "$(cat "${sd}devnum")" = "$dev_dec" ]; then
            ven=$(cat "${sd}idVendor"); pid=$(cat "${sd}idProduct")
            ser=$(cat "${sd}serial" 2>/dev/null)
            [ "$ven" = "0403" ] && [ "$pid" = "6011" ] && \
                printf "  %s  iSerial=%s\n" "$f" "$ser"
        fi
    done
done

echo
echo "Alveo cards visible to this pod:"
for d in /sys/bus/pci/drivers/xclmgmt/0000:* ; do
    [ -d "$d" ] || continue
    bdf=$(basename "$d")
    for sn in "$d"/xmc.*/serial_num ; do
        [ -f "$sn" ] && printf "  %s  serial=%s\n" "$bdf" "$(cat "$sn")"
    done
done
```

Sample output (from a real Pod on node-2-7 with xilinx.com/fpga_jtag: 1 ):

```
JTAG cables passed into this pod:
  /dev/bus/usb/001/006  iSerial=XFL1GHBRTQ42

Alveo cards visible to this pod:
  0000:21:00.0  serial=XFL1GHBRTQ42
  0000:a1:00.0  serial=XFL1H4XIZQLE
```

Note that the second Alveo card is still visible via /sys — sysfs is host-mounted — but only XFL1GHBRTQ42 is the one you can use, because that’s the one whose JTAG cable was passed in. The pod’s startup script can pick the matching BDF ( 0000:21:00.0 ) and operate on it.

## Example 4 — JTAG only, no FPGA (e.g. just talk to the SC over UART)

If all you need is the UART side of the FT4232H (no JTAG TAP access), smarter-devices is enough:

```
apiVersion: v1
kind: Pod
metadata:
  name: jtag-uart-only
  namespace: my-namespace
spec:
  restartPolicy: Never
  nodeSelector:
    fpga: "true"
  containers:
  - name: serial
    image: ubuntu:22.04
    command: ["sleep", "infinity"]
    resources:
      limits:
        smarter-devices/ttyUSB0: 1
        smarter-devices/ttyUSB1: 1
        memory: 1Gi
        cpu: "1"
```

You get /dev/ttyUSB0 and /dev/ttyUSB1 (host’s, not the pod’s own — same numbering). lsusb will list every FTDI on the host (sysfs is visible), but you can only open() the two ttyUSBs you requested. You cannot run JTAG operations through /dev/ttyUSB* ; that needs raw USB access ( /dev/bus/usb/... ), which is what xilinx.com/fpga_jtag mounts.

Important caveat: the smarter-device-manager regex in production today is ^ttyUSB[0-15]*$ , which only matches the device names ttyUSB0 , ttyUSB1 , ttyUSB5 , ttyUSB10 , ttyUSB11 , ttyUSB15 . Anything outside that set ( ttyUSB2 , ttyUSB3 , ttyUSB4 , …) is not exposed as a k8s resource even though the device file exists on the host. If you need access to those, contact the cluster admins on Nautilus Support .

## Verifying what you got

Once your pod is up:

```
# Should list the FPGA mgmt PFs (505c) and user PFs (505d) you were allocated.
lspci -d 10ee:

# Should list one FT4232H ("Xilinx A-U55C", ID 0403:6011) per JTAG you requested.
lsusb

# Read iSerials (Alveo card serials) on those FT4232H devices.
lsusb -v 2>/dev/null | grep -E "idVendor|idProduct|iSerial" | grep -B2 -A2 "FT4232\|0403:6011"

# If XRT is in your image:
source /opt/xilinx/xrt/setup.sh
xbutil examine     # confirms which card(s) you can actually use
xbmgmt examine     # mgmt side; shows serial numbers
```

If lsusb shows the FT4232H but /dev/bus/usb/... is empty (or you only got /dev/ttyUSB* ), you asked for smarter-devices/ttyUSB* only and JTAG operations (Vivado hw_server, OpenOCD, AMD’s xsdb ) will not work . Switch to xilinx.com/fpga_jtag for JTAG.

## XRT in your pod — what it is and how to use it

XRT (Xilinx Runtime) is the host-side userland that talks to your Alveo cards. The two binaries you’ll actually use are:

- xbutil — for the user PF ( 0000:<bb>:00.1 ). Loads .xclbin s, queries card state, validates the card. This is what your application uses indirectly via the runtime libraries.

- xbmgmt — for the management PF ( 0000:<bb>:00.0 ). Shell info, flashing, mgmt diagnostics.

XRT is installed on the host OS of every FPGA node (the device plugin won’t advertise cards without it). When your pod requests amd.com/xilinx_u55c_gen3x16_xdma_base_3-0 , kubelet mounts the host’s /dev/xclmgmt* and /dev/dri/renderD* into your container — but you still need XRT inside the pod to talk to those device nodes.

### Recommended pod image

The cluster’s Coder FPGA template image ( gitlab-registry.nrp-nautilus.io/nrp/coder-images/vivado-vitis ) has XRT 2.15.225 (2023.1) baked in, and the xilinx-tools PVC mounted at /tools/Xilinx/ provides Vivado 2021.2 / 2023.1 / 2023.2 and Vitis 2021.2 / 2023.2 (no Vitis 2023.1). You can use this image directly in a regular Pod or Job:

```
spec:
  imagePullSecrets:
  - name: gitlab-registry              # ask cluster admins if you don't have it in your ns
  containers:
  - name: dev
    image: gitlab-registry.nrp-nautilus.io/nrp/coder-images/vivado-vitis
    command: ["sleep", "infinity"]
    resources:
      limits:
        amd.com/xilinx_u55c_gen3x16_xdma_base_3-0: 1
        memory: 16Gi
        cpu: "4"
      requests:
        memory: 16Gi
        cpu: "4"
```

If you’d rather start from a stock Ubuntu and install XRT yourself, you have to ship the exact host-matching XRT deb ( 2.15.225 , 2.16.204 , or 2.19.194 depending on node — see the FPGA admindoc ) plus its dependency libraries. That’s harder than it sounds (Ubuntu 20.04-era boost / openssl, etc.); the Coder image is the path of least resistance.

### Commands you’ll actually run

```
# Get XRT on PATH and set lib paths
source /opt/xilinx/xrt/setup.sh

# What cards do I see? (user PF)
xbutil examine

# Detailed info on one card (replace BDF):
xbutil examine --device 0000:21:00.1

# Load an .xclbin onto a card (user PF)
xbutil program --device 0000:21:00.1 --user /path/to/kernel.xclbin

# Quick health validation (runs DMA + bandwidth tests against the card):
xbutil validate --device 0000:21:00.1

# Management side — shell + serial info:
xbmgmt examine
xbmgmt examine --device 0000:21:00.0 --report platform
```

xbutil examine (no --device ) lists every card visible to the pod with its XMC serial — which is your single source of truth for “which card did I actually get?” Match that serial against /sys/bus/usb/devices/<N-N>/serial (FTDI iSerial) and you’ve identified the physical hardware.

### Example: load an .xclbin and run a host app

The full inner loop, from a fresh pod:

```
# 1. Confirm what's in the pod
source /opt/xilinx/xrt/setup.sh
xbutil examine     # note the BDF and serial

# 2. Pull your .xclbin (from PVC, S3, or bake into image)
#    Example using a PVC mount or wget:
#    wget https://my-bucket.s3.us-west-2.amazonaws.com/kernels/vadd.xclbin -O /tmp/vadd.xclbin
ls -lh /tmp/vadd.xclbin

# 3. Program the card
xbutil program --device 0000:21:00.1 --user /tmp/vadd.xclbin

# 4. Run your host app (linked against libxrt_core/libxrt_coreutil)
./host_app /tmp/vadd.xclbin

# 5. (Optional) Read XMC sensors / power / temps while the kernel runs
xbutil examine --device 0000:21:00.1 --report electrical,thermal
```

Where to store .xclbin files: any of the usual options — a PVC in your namespace (durable, fast, doesn’t leave the cluster), an object-store bucket (S3 / Ceph RGW) you wget from, or baked into your own derived image. The cluster doesn’t enforce a convention; pick what fits your CI.

## Using Vivado/Vitis with the cluster license server

NRP runs a shared Xilinx FlexLM license server in-cluster so any pod (in any namespace) that needs to launch Vivado, Vitis, or vlm can do so without bringing its own license file. The server is reachable cluster-internally as:

```
[email protected]
```

### If you’re using the u55c-xilinx Coder template

The template’s pod spec already exports [email protected] as a container env, and the startup script writes a managed block into ~/.bashrc and ~/.zshrc that sources /opt/xilinx/xrt/setup.sh plus the chosen Vivado/Vitis settings64.sh and sets the LD_LIBRARY_PATH realloc workaround. So in any terminal opened inside the workspace (XFCE terminal via NoVNC, code-server terminal, kubectl exec -it ... bash ), you can just type:

```
vivado         # launches Vivado
vitis          # launches Vitis (if your chosen version has it)
vlm            # Vivado License Manager — confirms which features are served
xbutil examine # confirms what FPGA(s) you got
```

No export , no source — the env is in place. If you want a different Vivado/Vitis version than the one selected when you created the workspace, rebuild the workspace and pick a new value in the “Vivado / Vitis version” parameter, or manually source /tools/Xilinx/Vivado/<ver>/settings64.sh in your shell to override.

### If you’re on a custom pod (or an older Coder workspace)

The export + source dance is what you’d run by hand:

```
export XILINXD_LICENSE_FILE=2100@xilinxd.xilinx-dev
source /opt/xilinx/xrt/setup.sh
source /tools/Xilinx/Vivado/2023.1/settings64.sh    # or 2021.2 / 2023.2
vlm                                                   # confirms license served
vivado                                                # or vitis
```

If you do this often, add the same block to your image’s /etc/bash.bashrc or your container’s entrypoint so subshells inherit it.

vlm will connect to the server, list every feature available, and show its expiry date. If vlm lists your feature, you’re done — Vivado/Vitis will pick it up automatically from the same XILINXD_LICENSE_FILE env var.

If you have multiple license sources (your own personal license file and the cluster server), separate them with : (Linux) — FlexLM will try each in order:

```
export XILINXD_LICENSE_FILE=2100@xilinxd.xilinx-dev:/home/me/Xilinx.lic
```

### When the cluster server doesn’t have the license you need

The cluster license is sized for the AMD/Xilinx feature set most NRP users actually exercise (Vivado/Vitis core, the U55C XDMA shell, common IP cores). It is not a universal Vivado license — it doesn’t include every paid IP core AMD sells. If vlm connects but says “Feature not found” or Vivado fails at synthesis/implementation with Cannot checkout license :

- Get your own license, free, from AMD’s University Program. AMD’s University Program issues free academic licenses that include most evaluation IP. Apply with your .edu address. AMD will email you a .lic file tied to whatever hostid you specify (you can put your laptop’s MAC, or — for use inside an NRP pod — leave it node-locked to your username via a “user-based” license).

Get your own license, free, from AMD’s University Program. AMD’s University Program issues free academic licenses that include most evaluation IP. Apply with your .edu address. AMD will email you a .lic file tied to whatever hostid you specify (you can put your laptop’s MAC, or — for use inside an NRP pod — leave it node-locked to your username via a “user-based” license).

- Use it alongside the cluster server. Just prepend its path to XILINXD_LICENSE_FILE : Terminal window export XILINXD_LICENSE_FILE = / path / to / your / Xilinx . lic : 2100 @ xilinxd . xilinx-dev Vivado/Vitis will try your license first and fall back to the cluster server for everything else. Your personal license works the same way against NRP’s preinstalled Vivado and Vitis — you don’t need to bring tools, just the license.

Use it alongside the cluster server. Just prepend its path to XILINXD_LICENSE_FILE :

```
export XILINXD_LICENSE_FILE=/path/to/your/Xilinx.lic:2100@xilinxd.xilinx-dev
```

Vivado/Vitis will try your license first and fall back to the cluster server for everything else. Your personal license works the same way against NRP’s preinstalled Vivado and Vitis — you don’t need to bring tools, just the license.

### Where Vivado/Vitis live (and which version you get)

NRP uses Coder to mount the AMD toolchain into your pod read-only from a shared volume at /tools/Xilinx/ . The Coder FPGA templates wire this up automatically; if you build your own pod and want the same thing, ask the cluster admins on Nautilus Support for the PVC name and mount it readOnly: true .

Versions available today (under /tools/Xilinx/ ):

- Vivado : 2021.2 , 2023.1 (default in the Coder template), 2023.2

- Vitis : 2021.2 , 2023.2 (no 2023.1 — if you need Vitis, pick one of the matching pair)

Want a different Vivado/Vitis version? Two options:

- Ask the cluster admins to add it. Reach them on Nautilus Support — the toolchain is large but adding a new version is a one-time PVC update. This is the right path if more than one person on NRP will use that version.

- Run your own copy inside your namespace. Download Vivado/Vitis from AMD’s site, push it into a PVC under your namespace, and mount it into your pod. Slow first time, but completely self-service.

### Vivado doesn’t love being containerised — known workarounds

Vivado was designed for a desktop Linux install, not a container, and it sometimes trips on libc / glibc / library version mismatches inside a containerised environment. The most common report is a malloc() / realloc() crash or “corrupted size vs. prev_size” failure mid-synthesis or while loading the GUI.

The standard workaround is the LD_LIBRARY_PATH trick documented by AMD on their support forum:

LD_LIBRARY_PATH or other new shared libraries for 2021.2 missing

Concretely, before launching Vivado (the u55c-xilinx Coder template already does this in .bashrc using whichever Vivado version you picked):

```
export LD_LIBRARY_PATH=/tools/Xilinx/Vivado/$XILINX_VIVADO_VERSION/lib/lnx64.o:$LD_LIBRARY_PATH
# (replace $XILINX_VIVADO_VERSION with 2021.2 / 2023.1 / 2023.2 if not set)
vivado
```

If that still doesn’t get you a stable Vivado run, the escape hatch is to run Vivado inside a KubeVirt VM in your namespace instead of inside a regular pod. That sidesteps every container/host glibc interaction at the cost of having to install Vivado yourself inside the VM. It’s not trivial but it is sometimes the only way certain Vivado releases will stay up. The general recipe for an Ubuntu VM under KubeVirt on NRP is here:

Virtualization — Ubuntu

From inside that VM you can install Vivado normally ( ./xsetup ), then point it at the cluster license server the same way ( export [email protected] ). The VM still has cluster DNS so xilinxd.xilinx-dev resolves.

### Quick sanity check from a fresh pod

```
# 1. server reachable?
getent hosts xilinxd.xilinx-dev || nslookup xilinxd.xilinx-dev
nc -vz xilinxd.xilinx-dev 2100

# 2. license features visible?
#    (Skip the export/source if you're on the u55c-xilinx Coder template — already done in .bashrc.)
export XILINXD_LICENSE_FILE=2100@xilinxd.xilinx-dev
source /tools/Xilinx/Vivado/2023.1/settings64.sh
vlm    # GUI; or use lmutil:
/tools/Xilinx/Vivado/2023.1/tps/lnx64/lmutil/lmutil lmstat -a -c "$XILINXD_LICENSE_FILE"
```

If lmstat -a lists the features and you’ve sourced settings64.sh , both Vivado and Vitis will pick up the license automatically — no per-tool configuration needed.

## Flashing a card’s base shell from a pod

### Step 1 — verify you got the card you think you got

Inside your pod (with both amd.com/xilinx_u55c_* and xilinx.com/fpga_jtag requested):

```
source /opt/xilinx/xrt/setup.sh

# Visible Alveos and their XMC serials
for d in /sys/bus/pci/drivers/xclmgmt/0000:* ; do
  bdf=$(basename "$d")
  for sn in "$d"/xmc.*/serial_num ; do
    [ -f "$sn" ] && printf "%s  serial=%s\n" "$bdf" "$(cat "$sn")"
  done
done

# JTAG cable allocated to this pod and its iSerial
for f in /dev/bus/usb/*/* ; do
    bus=$(basename "$(dirname "$f")"); dev=$(basename "$f")
    bus_dec=$((10#$bus)); dev_dec=$((10#$dev))
    for sd in /sys/bus/usb/devices/*/; do
        [ -f "${sd}busnum" ] || continue
        if [ "$(cat "${sd}busnum")" = "$bus_dec" ] && [ "$(cat "${sd}devnum")" = "$dev_dec" ]; then
            ven=$(cat "${sd}idVendor"); pid=$(cat "${sd}idProduct")
            [ "$ven" = "0403" ] && [ "$pid" = "6011" ] && \
                printf "%s  iSerial=%s\n" "$f" "$(cat "${sd}serial")"
        fi
    done
done
```

The serial= value from xclmgmt and the iSerial= of the FT4232H must match the card you intend to flash. That string (e.g. XFL1GHBRTQ42 ) is your single point of truth — it’s printed on the card label and shows up in both XRT and lsusb . If the BDF you’re about to flash isn’t paired with the iSerial you agreed on with the admin, stop.

### Step 2 — flash

```
# Example: card 0000:21:00 with serial XFL1GHBRTQ42
sudo /opt/xilinx/xrt/bin/xbmgmt program \
     --base \
     --device 0000:21:00.0 \
     --image  xilinx_u55c_gen3x16_xdma_base_3
```

Each card takes 30–45 minutes . Don’t kill the process. Multiple cards on the same host can flash in parallel — each xbmgmt drives its own card. Output ends with something like Cold reboot required.

### Step 3 — tell the admin to power cycle

A warm reboot is not enough — the flash partition isn’t loaded until the chassis power-cycles. Tell the admin (on the same Nautilus Support thread you opened the session in) that the flash is done and they can ipmitool power cycle the node now. Once it’s back up they’ll verify with xbutil examine ( Device Ready: Yes on the new shell).

If your flash fails (timeouts, mid-write power loss, wrong image), the card is in xilinx_u55c_recovery (golden mode) — also recoverable, but only via a clean reflash. Don’t try to fix it yourself; reopen the ticket and the admins have a runbook in the FPGA admindoc .

## Troubleshooting

Things that go wrong, and how to debug them from inside the pod.

### xbutil examine reports 0 devices found

Either:

- The pod didn’t actually request amd.com/xilinx_u55c_gen3x16_xdma_base_3-0 (check kubectl describe pod ), or

- The card is in golden/recovery mode — the XMC subdev didn’t load. Check xbmgmt examine -d <BDF> --report platform ; if it says xilinx_u55c_recovery , the shell needs reflashing. Do not try to reflash from a regular pod; contact the cluster admins on Nautilus Support .

- Less commonly, the host’s xclmgmt kernel module isn’t loaded (host-side issue). ls /sys/bus/pci/drivers/xclmgmt/ from the pod — if it’s empty, the host needs admin attention.

### lspci -d 10ee: shows nothing inside my pod

The pod doesn’t have the resource. lspci -d 10ee: -nD looks at the host’s PCI tree (sysfs is mounted), so if it shows nothing, you literally have no FPGA allocation. Check resources.limits has the AMD plugin’s resource name spelled exactly: amd.com/xilinx_u55c_gen3x16_xdma_base_3-0 .

### Wrong card got allocated to my pod

The AMD device plugin doesn’t honour any pin hint — if you asked for 1 and the host has 2, you get one of them and you don’t get to choose. Two fixes:

- Pin to a single-card host ( node-2-9 , node-2-10 ) where there’s only one possible answer.

- Request all cards on the host (e.g. 2 on node-2-7 ) — then both serials are yours and you pick the right one in code.

The runtime-pairing script in Example 3 is how you tell which BDF corresponds to which iSerial inside the pod.

### My pod scheduled to the wrong node

If nodeSelector: kubernetes.io/hostname: <fqdn> didn’t pin it where you wanted, double-check the FQDN spelling against kubectl get nodes -o name . Typos here are silent — Kubernetes will happily wait forever in Pending with no scheduler event explaining why.

If the pod is Pending with Insufficient amd.com/xilinx_u55c_gen3x16_xdma_base_3-0 , every advertised card on that node is currently in use. kubectl describe node <fqdn> | grep xilinx shows allocatable vs allocated.

### lsusb lists FT4232H devices but /dev/bus/usb/... is empty

You asked for smarter-devices/ttyUSB* (UART only), not xilinx.com/fpga_jtag (raw USB). Vivado hw_server / OpenOCD / xbmgmt program will not work with ttyUSB* . Switch the request to xilinx.com/fpga_jtag: N and re-create the pod. (Sysfs lists every USB device on the host — that’s why lsusb looks like it’s working; but only what’s actually under /dev/bus/usb/ is openable.)

### xbutil program --user says “Failed to program device”

- .xclbin was built for a different shell than what’s flashed on the card. Check xbmgmt examine -d <BDF>.0 --report platform for the card’s actual shell, and rebuild the .xclbin against it.

- The .xclbin is corrupt or partially downloaded. xclbinutil --info -i my.xclbin will tell you if it parses.

- Another tenant on the host has the card programmed and you raced. (Unlikely if you have an exclusive allocation, but possible if you’re sharing a host through some custom mechanism.)

### vlm / Vivado says “Cannot connect to license server”

DNS: getent hosts xilinxd.xilinx-dev should resolve. Connectivity: nc -vz xilinxd.xilinx-dev 2100 should succeed. If either fails, NRP’s license server is down — contact the cluster admins on Nautilus Support . If both succeed and Vivado still rejects the license, check vlm for whether your specific feature is in the served list; you may need to fall back to a personal AMD University Program license (see the license section above).

### Vivado crashes mid-synthesis with realloc(): invalid pointer

Known containerisation issue. Try the LD_LIBRARY_PATH workaround (see Vivado containerisation ). If that doesn’t help, run Vivado in a KubeVirt VM instead of a pod.

## Why is the model like this?

amd.com/xilinx_u55c_gen3x16_xdma_base_3-0 is registered by AMD’s k8s-device-plugin running as the xilinx-device-plugin-daemonset DaemonSet. xilinx.com/fpga_jtag is registered by KubeVirt’s virt-handler based on the cluster’s KubeVirt CR permittedHostDevices.usb config (which currently matches any FTDI FT4232H — vendor 0403 , product 6011 ). The two services discover hardware independently and have no shared notion of “this USB device belongs to this PCIe device.” That’s why the matching has to be done by the pod itself — usually trivially, because sysfs gives you both serials.
