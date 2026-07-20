# Getting Started with NRP Nautilus

Source: https://nrp.ai/documentation/userdocs/start/getting-started

# Getting Started with NRP Nautilus

### Get access and log in

If you are a new user and want to access the NRP Nautilus cluster, follow the steps below.

- Point your browser to the NRP Nautilus portal .

Point your browser to the NRP Nautilus portal .

- On the portal page, click on the Log In button at the top right corner.

On the portal page, click on the Log In button at the top right corner.

- You will be redirected to the CILogon page, where you have to Select an Identity Provider .

You will be redirected to the CILogon page, where you have to Select an Identity Provider .

- Select your institution (for example: University Name) from the menu and click the Log On button. If your institution is using CILogon as a federated certification authority, it will be on the menu. Select the name of your institution and use either a personal account or an institutional G-suite account. This is usually your institutional account name (email) and a password associated with it. If your institution is not in the list, you may be able to use the Microsoft entry. If your university uses Microsoft’s Active Directory for user management (common if your campus uses Office 365 or related products), then you can login with your institutional credentials at the Microsoft login prompt. If your institution is not in the CILogon dropdown, and Microsoft also doesn’t work, you can select Google or Github .

Select your institution (for example: University Name) from the menu and click the Log On button.

- If your institution is using CILogon as a federated certification authority, it will be on the menu. Select the name of your institution and use either a personal account or an institutional G-suite account. This is usually your institutional account name (email) and a password associated with it.

- If your institution is not in the list, you may be able to use the Microsoft entry. If your university uses Microsoft’s Active Directory for user management (common if your campus uses Office 365 or related products), then you can login with your institutional credentials at the Microsoft login prompt.

- If your institution is not in the CILogon dropdown, and Microsoft also doesn’t work, you can select Google or Github .

- After a successful authentication, you will log in to the portal and your account will be created if it was not created before.

After a successful authentication, you will log in to the portal and your account will be created if it was not created before.

- If you are a student , please contact your research supervisor and ask them to add you to their namespace . Once you are added to a namespace, your status will change to a cluster user and you will get access to all namespace resources.

If you are a student , please contact your research supervisor and ask them to add you to their namespace . Once you are added to a namespace, your status will change to a cluster user and you will get access to all namespace resources.

- If you are a faculty member, university staff member, or postdoc starting a new project and need your own namespace — either for yourself or your research group — you can request to be promoted to a namespace admin in Nautilus Support . Also let us know the desired name for your group (usually the department name). You can use lowercase letters, numbers, and dashes only. Choose clear, descriptive names (avoid generic ones like kubernetes-ai , testing-group , llm-access ). To see the existing names for reference, please visit this visualization tree . As an admin , you will have the ability to: Create multiple namespaces. Invite other users to your namespace(s). We’re handling the namespaces management as a hierarchical model where we delegate the management of certain parts to the admins who can then further delegate the responsibilities.. With your request to become an admin, please let us know your current affiliation and where you see yourself fitting in this structure. You can simply own a single namespace under your university branch for small experiments or manage multiple different namespaces for large departments or groups of students. Read more

If you are a faculty member, university staff member, or postdoc starting a new project and need your own namespace — either for yourself or your research group — you can request to be promoted to a namespace admin in Nautilus Support . Also let us know the desired name for your group (usually the department name). You can use lowercase letters, numbers, and dashes only. Choose clear, descriptive names (avoid generic ones like kubernetes-ai , testing-group , llm-access ). To see the existing names for reference, please visit this visualization tree . As an admin , you will have the ability to:

- Create multiple namespaces.

- Invite other users to your namespace(s).

We’re handling the namespaces management as a hierarchical model where we delegate the management of certain parts to the admins who can then further delegate the responsibilities..

With your request to become an admin, please let us know your current affiliation and where you see yourself fitting in this structure. You can simply own a single namespace under your university branch for small experiments or manage multiple different namespaces for large departments or groups of students.

Read more

- Access your namespace(s). If you have become a namespace admin , you can start creating your own namespaces at this time by going to the Namespaces manager section on the portal. You can add other users on the same page after they have logged in to the portal. If you got added to a namespace as a user , you can verify it by going to the Namespaces manager tab after logging in to the portal. The namespaces you’re a member of will be marked in bold.

Access your namespace(s).

- If you have become a namespace admin , you can start creating your own namespaces at this time by going to the Namespaces manager section on the portal. You can add other users on the same page after they have logged in to the portal.

- If you got added to a namespace as a user , you can verify it by going to the Namespaces manager tab after logging in to the portal. The namespaces you’re a member of will be marked in bold.

- Make sure you read the cluster policies before starting to use it.

Make sure you read the cluster policies before starting to use it.

- Make sure you’re on Nautilus Support. All Nautilus and NRP users are expected to join for user support and real-time updates.

Make sure you’re on Nautilus Support. All Nautilus and NRP users are expected to join for user support and real-time updates.

### Cluster access via kubectl

- Install the Kubernetes command-line tool, kubectl from the official instructions of each OS.

Install the Kubernetes command-line tool, kubectl from the official instructions of each OS.

- Install kubelogin plugin Download kubelogin Example for Linux or macOS ( curl , jq , and unzip should be installed): Terminal window # OS_ARCHITECTURE should be in the format `amd64` or `arm64` # For Debian/Ubuntu - change as adequate for RHEL or macOS OS_ARCHITECTURE = " $( dpkg --print-architecture ) " # Change to `darwin` for macOS OS_NAME = " linux " # Install kubelogin KUBELOGIN_VERSION = " $( curl -fsSL " https://api.github.com/repos/int128/kubelogin/releases/latest " | jq -r ' .tag_name ' ) " curl -o kubelogin.zip -fSL " https://github.com/int128/kubelogin/releases/download/${ KUBELOGIN_VERSION }/kubelogin_${ OS_NAME }_${ OS_ARCHITECTURE }.zip " unzip kubelogin.zip kubelogin chmod +x ./kubelogin # Replace `/usr/local/bin` to `~/.local/bin` (create the directory when nonexistent) and set `export PATH="~/.local/bin:${PATH}"` for local user sudo mv ./kubelogin /usr/local/bin/kubectl-oidc_login sudo chown root: /usr/local/bin/kubectl-oidc_login rm -f kubelogin.zip

Install kubelogin plugin

Download kubelogin

Example for Linux or macOS ( curl , jq , and unzip should be installed):

```
# OS_ARCHITECTURE should be in the format `amd64` or `arm64`
# For Debian/Ubuntu - change as adequate for RHEL or macOS
OS_ARCHITECTURE="$(dpkg --print-architecture)"
# Change to `darwin` for macOS
OS_NAME="linux"

# Install kubelogin
KUBELOGIN_VERSION="$(curl -fsSL "https://api.github.com/repos/int128/kubelogin/releases/latest" | jq -r '.tag_name')"
curl -o kubelogin.zip -fSL "https://github.com/int128/kubelogin/releases/download/${KUBELOGIN_VERSION}/kubelogin_${OS_NAME}_${OS_ARCHITECTURE}.zip"
unzip kubelogin.zip kubelogin
chmod +x ./kubelogin
# Replace `/usr/local/bin` to `~/.local/bin` (create the directory when nonexistent) and set `export PATH="~/.local/bin:${PATH}"` for local user
sudo mv ./kubelogin /usr/local/bin/kubectl-oidc_login
sudo chown root: /usr/local/bin/kubectl-oidc_login
rm -f kubelogin.zip
```

- Save the config file as config (without any extension) and put it in your $HOME/.kube folder. Download Config File This folder may not exist on your machine, to create it execute: Terminal window mkdir ~/.kube Finally, you should have the Nautilus Kubernetes config on your machine (laptop, desktop) as ~/.kube/config (e.g., curl -o ~/.kube/config -fSL "https://nrp.ai/config" )

Save the config file as config (without any extension) and put it in your $HOME/.kube folder.

Download Config File

This folder may not exist on your machine, to create it execute:

```
mkdir ~/.kube
```

Finally, you should have the Nautilus Kubernetes config on your machine (laptop, desktop) as ~/.kube/config (e.g., curl -o ~/.kube/config -fSL "https://nrp.ai/config" )

- Cross-platform kubelogin fixes (WSL / Linux / Windows / macOS) No local browser available (remote console, use the link in Please visit the following URL in your browser: to login with CILogon): Terminal window --grant-type = device-code --skip-open-browser Browser issues (won’t launch or opens incorrectly): Terminal window --browser-command = " /mnt/c/Program Files/Google/Chrome/Application/chrome.exe " (Windows WSL: points to Windows Chrome) Port binding errors ( port 8000 already in use ): Terminal window --listen-address = 0.0.0.0:18000 (change to any unused port) Example config snippet: args : - oidc-login - get-token - --browser-command="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" - --listen-address=0.0.0.0:18000 - --token-cache-storage=disk You can store the token cache to the OS keyring for enhanced security. args : - oidc-login - get-token - --token-cache-storage=keyring

Cross-platform kubelogin fixes (WSL / Linux / Windows / macOS)

- No local browser available (remote console, use the link in Please visit the following URL in your browser: to login with CILogon): Terminal window --grant-type = device-code --skip-open-browser

No local browser available (remote console, use the link in Please visit the following URL in your browser: to login with CILogon):

```
--grant-type=device-code
--skip-open-browser
```

- Browser issues (won’t launch or opens incorrectly): Terminal window --browser-command = " /mnt/c/Program Files/Google/Chrome/Application/chrome.exe " (Windows WSL: points to Windows Chrome)

Browser issues (won’t launch or opens incorrectly):

```
--browser-command="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
```

(Windows WSL: points to Windows Chrome)

- Port binding errors ( port 8000 already in use ): Terminal window --listen-address = 0.0.0.0:18000 (change to any unused port)

Port binding errors ( port 8000 already in use ):

```
--listen-address=0.0.0.0:18000
```

(change to any unused port)

Example config snippet:

```
args:
  - oidc-login
  - get-token
  - --browser-command="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
  - --listen-address=0.0.0.0:18000
  - --token-cache-storage=disk
```

You can store the token cache to the OS keyring for enhanced security.

```
args:
  - oidc-login
  - get-token
  - --token-cache-storage=keyring
```

- Make sure you are using the correct config file. Run the following command to list available Kubernetes contexts: Get Contexts $ kubectl config get-contexts CURRENT NAME CLUSTER AUTHINFO NAMESPACE * nautilus   nautilus   oidc If you have access to multiple Kubernetes clusters, you need to choose use-context nautilus by doing Set Context kubectl config use-context nautilus

Make sure you are using the correct config file.

- Run the following command to list available Kubernetes contexts: Get Contexts $ kubectl config get-contexts CURRENT NAME CLUSTER AUTHINFO NAMESPACE * nautilus   nautilus   oidc

Run the following command to list available Kubernetes contexts:

```
$ kubectl config get-contexts
CURRENT   NAME       CLUSTER    AUTHINFO   NAMESPACE
*         nautilus   nautilus   oidc
```

- If you have access to multiple Kubernetes clusters, you need to choose use-context nautilus by doing Set Context kubectl config use-context nautilus

If you have access to multiple Kubernetes clusters, you need to choose use-context nautilus by doing

```
kubectl config use-context nautilus
```

- Issue the kubectl command. It will authenticate via CiLogon by opening the browser window, and close one in the end. kubectl get nodes

Issue the kubectl command. It will authenticate via CiLogon by opening the browser window, and close one in the end.

```
kubectl get nodes
```

- Verify cluster access using kubectl . Run the following command on your terminal. Get Pods kubectl get pods -n <YOUR_NAMESPACE> If you see the message “No resources found in your namespace” it means there are no pods in your namespace yet. This indicates that you have access to the resources of your namespace.

Verify cluster access using kubectl . Run the following command on your terminal.

```
kubectl get pods -n <YOUR_NAMESPACE>
```

If you see the message “No resources found in your namespace” it means there are no pods in your namespace yet. This indicates that you have access to the resources of your namespace.

- If you know you’re a member of a namespace, you can set it as default. kubectl config set contexts.nautilus.namespace <YOUR NAMESPACE>

If you know you’re a member of a namespace, you can set it as default.

```
kubectl config set contexts.nautilus.namespace <YOUR NAMESPACE>
```

### Updating namespace membership

By default the access token expires in half an hour and is automatically updated after that. If you need to update one sooner (for example, you were added to a new namespace), you can invalidate the token:

```
kubectl oidc-login clean
```

After that any kubectl command will trigget getting the new token. (F.e. kubectl get nodes )

### Use the Cluster

- Read the Using Nautilus page to learn how to use the cluster.

Read the Using Nautilus page to learn how to use the cluster.

- To learn more about Kubernetes you can look at our tutorial .

To learn more about Kubernetes you can look at our tutorial .

- Other helpful resources: kubectl Tool Overview and Cheatsheet Kubernetes Basics from Kubernetes project Kubernetes Official Tutorials Please note that not all examples will work in our cluster because of security policies. You are limited to seeing what’s happening in your own namespace, and nobody else can see your running pods.

Other helpful resources:

- kubectl Tool Overview and Cheatsheet

- Kubernetes Basics from Kubernetes project

- Kubernetes Official Tutorials

Please note that not all examples will work in our cluster because of security policies. You are limited to seeing what’s happening in your own namespace, and nobody else can see your running pods.

### GUI tools for Kubernetes

You might want to try one of these GUI tools for Kubernetes:

- K9s - Console graphical user interface

- Visual Studio Code - Instructions below

- Lens - Graphical user interface

They will all use your config file in the default location to get access to the cluster.

#### Visual Studio Code

Install both the Kubernetes and Remote Development extensions.

After configuring the requirements below and setting the namespace (look at the bottom of the interface after entering the Kubernetes tab), right-click the Deployment, Pod, or any other resource, and press Attach Visual Studio .

Two things are required to work:

- The Nautilus cluster config file must be located precisely in ~/.kube/config (Linux, macOS), or %USERPROFILE%\.kube\config (Windows). Using --kubeconfig or manually specifying the kubeconfig file path in Visual Studio Code will not work.

- The interface prompt for installing kubectl within Visual Studio Code will NOT work for accessing the resource. Both kubectl and kubectl-oidc_login executable files must be in the PATH .

- For Windows , an easy way to make kubectl and kubectl-oidc_login work is to copy the two .exe executable files into %LOCALAPPDATA%\Programs\Microsoft VS Code\bin or C:\Program Files\Microsoft VS Code\bin (depending on the Visual Studio Code installation), where these directories are already added into the PATH in Windows.
