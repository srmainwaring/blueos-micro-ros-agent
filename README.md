# BlueOS micro-ROS Agent

BlueOS Extension to run a micro-ROS agent on the host computer to connect
to an autopilot supporting DDS.

## Usage

Information for users

- Open the micro-ROS Agent tab
- Complete these fields
  - Transport: udp4
  - Port: 2019
  - Verbose: 4
- Click the "Save" button to save settings
- Click the "Run" button to start the micro-ROS Agent

## Developer Information

To build the docker image and upload to Docker Hub:

```bash
docker buildx build --platform linux/amd64,linux/arm/v7,linux/arm64/v8 . -t {your_dockerhub_id}/blueos-micro-ros-agent:0.0.0 --output type=registry
```

To manually install the extension in BlueOS:

- Open the BlueOS Extensions tab, select "Installed"
- Push the "+" button on the bottom right
- Under "Create Extension" complete these fields
  - Extension Identifier: {your_dockerhub_id}.blueos-micro-ros-agent
  - Extension Name: micro-ROS Agent
  - Docker image: {your_dockerhub_id}/blueos-micro-ros-agent
  - Dockertag: 0.0.0
  - Settings: add the settings below in the editor

```json
{
  "NetworkMode": "host",
  "HostConfig": {
    "Privileged": true,
    "Binds": [
      "/usr/blueos/extensions/micro-ros-agent/settings:/app/settings",
      "/usr/blueos/extensions/micro-ros-agent/logs:/app/logs",
      "/dev:/dev:rw"
    ],
    "CpuQuota": 100000,
    "CpuPeriod": 100000,
    "NetworkMode": "host",
    "PortBindings": null
  }
}
```
