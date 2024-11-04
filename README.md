# TuneCube

TuneCube is dedicated software for DJs, dance event organizers, and party attendees. It continuously listens to the music playing on the dance floor and provides information about the current and previous song titles (like Shazaam). Detected titles are added to a dedicated Spotify playlist, accessible by scanning a QR code displayed on the screen.

## Purpose

The goal of TuneCube is to make life easier for DJs, organizers, and event attendees. 
- **For DJs**: You can easily share a link to your playlist with anyone interested.
- **For Organizers**: If multiple DJs are performing at an event, you can provide a complete playlist of the entire event.
- **For Attendees**: You can access the whole event playlist or simply focus on dancing, knowing that you’ll find the name of that one special song later on the display screen.

## Main Features

- **Song Recognition**: Utilizes Shazam to recognize songs being played.
- **Spotify Integration**: Adds recognized songs to a dedicated Spotify playlist.
- **Playlist Sharing**: Share the playlist using a QR code displayed on an external screen.

## Technologies Used

- **Docker**: Containerized infrastructure for easy deployment.
- **Backend**: Python 3.11, Flask, and Shazamio for song recognition.
- **Frontend**: Node.js and React.
- **GUI Environment**: Ubuntu, XOrg, and Chromium.

## Installation and Setup

### Prerequisites
- A board like Raspberry Pi with a clean installation of Ubuntu Server.
- **Software Requirements**: Xorg, PulseAudio, and NetworkManager.
- **External Components**:
  - Sound card with microphone input and dedicated microphone.
  - External display for show the user interface and QR code.
  - 
### Setup Instructions
1. Clone the repository and navigate to the project directory.
2. Configure the `.env` file with your Spotify API keys and path to the PulseAudio socket on your host machine.
4. Build and start the project using Docker Compose:
   ```bash
   docker-compose up --build
5. Ensure that your external sound card and display are properly connected and configured.

### Hardware Prototype (Example Setup)

- Display: Aputure V-Screen VS-2 FineHD (~600 PLN)
- Board: Raspberry Pi 4 8GB (~350 PLN)
- Microphone: BOYA BY-MM1 (~100 PLN)
- Sound Card USB with Mic Input: Unitek Y-247A (~50 PLN)
- Wireless USB Adapter: Lanberg NC-1200-WI (~50 PLN)
- DC-DC Converter 12V - 5V USB-C (~30zl)
- 12V Power Supply: POS-50-12-C2 12V/4,2A/50,4W  (~50 PLN)

![Alt Text](https://radoslaw.gierwialo.com/tunecube/poc.png)

For those interested, I am providing the [Autodesk Fusion 3D file with the 3D model for the enclosure used in the prototype](https://radoslaw.gierwialo.com/tunecube/body.f3z). Feel free to download and modify it as needed for your own projects.



## Disclaimer

This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the author be liable for any claim, damages, or other liability arising from the use of this software.

## Contributing

Contributions are welcome! If you would like to contribute, feel free to fork the repository, create a feature branch, and submit a pull request. Whether it’s fixing a bug, adding new features, or improving the documentation, your help is greatly appreciated. Let’s make TuneCube even better together!

## Future Updates

TuneCube is currently in a proof-of-concept stage but is under active development. Planned updates include improved UI, and additional customization options for users.

## License

TuneCube is licensed under the GNU Affero General Public License (AGPL-3.0). This license ensures that any modifications or forks must credit the original author and the TuneCube project.

## Acknowledgements

Thank you for using TuneCube! Contributions, feedback, and suggestions are always welcome. If you have ideas for improvements or want to report a bug, feel free to open an issue or submit a pull request.


