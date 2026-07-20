# ESnet SmartNIC FPGA - Building

Source: https://nrp.ai/documentation/userdocs/fpgas/esnet_building

# ESnet SmartNIC FPGA - Building

## Building (Notebook 1/3): Building Artifacts & Bitstream from P4 Logic

This notebook is Part 2 of the ESnet SmartNIC Tutorial on NRP series. It continues from Notebook 1 to provide an example for building the FPGA logic from our SmartNIC P4 code.

### Test Environment

This notebook was tested on the National Research Platform (NRP) using the AMD/Xilinx Alveo U55C FPGA and Vivado 2023.1 . The Kubernetes pods were provisioned by Coder .

If you run into any issues, please refer to the official NRP Documentation , or reach out to us via Nautilus Support or email .

Before using the ESnet SmartNIC tools, kindly review the official ESnet SmartNIC Copyright Notice .

### Step 1: Set up environment

Do not remove pre-existing files. We will be continuing from where we left off with Notebook 1.

```
echo "$BASH_VERSION"
```

If the above command doesn’t show a bash version, you may be running with a Python kernel. Please switch to a Bash kernel.

```
cd ~/esnet-smartnic/esnet-smartnic-hw/examples/p4_only
ls
```

Clone the esnet-smartnic-hw repository from ESnet. Checkout at the latest tested commit.

### Step 2: Configure the Makefile

```
cat Makefile
```

```
sed -i 's/^#export BOARD := au280/export BOARD := au55c/' Makefile
```

```
cat Makefile | grep -i BOARD
```

### Step 3: Build the artifacts

Make sure that Vivado 2023.1 is used. (The versioning depends on the commit of the repo that we use.)

Make sure that the license server is correctly pointed to by pointing XILINXD_LICENSE_FILE to [email protected] .

This service is consistent across the Nautilus cluster. 2100 is the port on the license server pod where the server runs. xilinxd is the name of the service xilinx-dev is the name of the namespace

You can always test the license by going on the noVNC Desktop, and running the source command, then running vlm . This will bring up the Vivado License Manager.

```
source /tools/Xilinx/Vivado/2023.1/settings64.sh
export XILINXD_LICENSE_FILE=2100@xilinxd.xilinx-dev
```

Please read carefully:

The make command will start the process of compiling the logic from P4 to the packaged artifacts (zip archive containing the bitstream and other relevant files). This process involves various steps like synthesis, implementation, and exporting hardware. This takes on average * 5 hours . There are multiple factors that affect the time including the memory requested for the pod , and the current speed and health of the filesystem that hosts the Xilinx tools.

When not comfortable running the make command directly in Jupyter, one has various ways of running the command, including:

1- In a noVNC terminal window (on XFCE terminal).

2- Directly in the Jupyter notebook.

3- In the Jupyter Bash terminal.

4- In the Coder terminal window.

5- Inside VSCode.

6- Using ssh from the coder cli .

7- Using the kubectl exec command.

For the sake of demonstration, we are simply going to use make . However, if the notebook, kernel and/or command gets interrupted.

```
#make
```

Considering how long the logs are, we recommend running make > building.logs .

After the command finished, you will see the artifacts in `artifacts/p4_only..

Now we reach the end of writing building the artifacts from the P4 logic.

This notebook is part 2 out of 3 in the ESnet SmartNIC Tutorial on NRP series.

This was last modified on March 4th, 2025.

For any inquiries, questions, feedback, please contact: [email protected]
