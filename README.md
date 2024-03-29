# Cloud Inference Server - Distributed ML Computation

Web server built to serve machine learning inference tasks, allowing clients to leverage remote computing resources. Aka allowing my gaming computer to support the home infrastructure when I'm not using it.

For more information, please see [Hobby Automation](http://hobbyautomation.com/).
 
![Hobby Automation Chart](https://i.imgur.com/m3n26FX.png "Hobby Automation Chart")

[![Hobby Automation Website](https://i.imgur.com/BMUoGOi.png "Hobby Automation Website")](http://hobbyautomation.com/)

---

### Adding Modules:

The architecture of this software has been designed from the ground up to eliminate duplicate code and emphasize simplicity of adding new modules. Here's what you need to do. 

1. Import the repo of your module in the parent directory up from this one (src).
2. Make sure you have an up-to-date kotakee_companion repo if you're using it's code for endpoint functionality. 
3. Define a new endpoint in service_definitions, including the name of the function you plan to use. 
4. Create a new module in one of the module subfolders.
5. Add an entry in handler_definitions for your handler pointing out the name of the class of your new module. 

6. (Docker) Update the Dockerfile to do the following:

   - Copy your new repository

   - Install the requirements.txt of your new repository

   - Copy any files from kotakee_companion that you need.

And that's it!

---

### Usage:

To host the cloud inference server, make sure you follow these steps:

1. Install pytorch. I'm assuming you're hosting this on a machine with a decent GPU for machine learning inference, so go to pytorch.org and get the best command relative to your CUDA version. 

2. Install everything required. Run:

   pip install -r requirements.txt 

3. Run the server. 

   python cloud_wed_service.py

---

### Usage: Docker Container

To create a docker container, you'll need to take a few simple steps.

1. Copy the up-to-date Dockerfile to the parent directory (src) that contains all of the source repositories specified in the file.

2. Run the following to build the container image: 

   docker build --tag cloud_inference_server:1.0 .

3. Once the container image has been created, run it. You can do this from docker desktop.

---

### Prerequisites

1. pip3 install -r requirements.txt 

2. For machine pianist to wav, sf2_loader requires ffmpeg. 