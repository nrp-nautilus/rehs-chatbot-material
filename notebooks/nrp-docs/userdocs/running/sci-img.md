# Scientific Images

Source: https://nrp.ai/documentation/userdocs/running/sci-img

# Scientific Images

This page is mostly related to our Official JupyterHub , but all images can be also used in other pods deployed directly on the cluster.

There are two main projects providing the stack of images:

Docker Stack

B-Data

Both projects now support CUDA and ARM. Docker stack only has CUDA in TensorFlow and PyTorch variants.

The list of NRP-provided images and registry links are available in our GitLab registry :

The NRP image with additional libraries (gitlab-registry.nrp-nautilus.io/nrp/scientific-images/python) is based on Docker Stack TensorFlow and PyTorch, with additional packages.

NOTE: If you are using the VS Code editor with a Jupyter Notebook, use the base Python Environment as the kernel. Moreover, do not use the /usr/bin/python / /usr/bin/python3 Python executable. Instead, use python or python3 without the path.

Refer to https://gitlab.nrp-nautilus.io/nrp/scientific-images/python for the list of packages installed.

We can add more libraries to this image by requesting in Nautilus Support .

The Desktop image has the X11 Window system installed and you can launch the GUI interface in Jupyter with this image. It’s based on the Minimal stack.
