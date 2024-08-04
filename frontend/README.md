# frontend/
The frontend/ directory has the web UI for humans.

## Build
### Note: 
The latest build is available in my public repository for this challenge. All builds are derived from my private **morezio/envs:u_dev**, which is based on **ubuntu:jammy**, adding commodities for development (ohmyzsh, auto-suggestions, poetry, docker client [to mount the socket], etc.) as seen in the history of the layers.
```zsh

# Make sure to be located at /storimages 
docker build -t <your-repository>/storimages:fe_dev -f frontend.dockerfile .
```
## Pull
Latest build is online!
```zsh
docker pull morezio/storimages:fe_dev
```
## Try it!
First you need to create an instance of the image like:
```zsh
# Up to this edition, the UI was still under development so just the upload drag and drop works
docker run -d -p 80:80 --name be morezio/storimages:fe_dev

```
Then open any browser you like provided you're running the container locally or forwarding it and take a look into [localhost](http://localhost:80). 

As mentioned in both the summary and the sketch of the roadmap, I intended to make the UI appealing and possible to process batches of pictures from the first dev releases, but I ran into a pretty busy week and couldn't allocate much time but at night. 

Anyhow, the idea was to have a preview just above the drag and drop once dropped into the area or clicked for the finder / nautilus / file explorer to open and pick 1 file, later on several. Also to be able to select from a dropdown some presets like:
- Photo galleries = 120x90
- Video = 160x120
- Social media profile picture = 100x100
- Online store - small = 80x80
- Online store - large = 150x150
- Icons = 96x96

And in the stable release, allow for custom per picture and be able to remove background thanks to an API.

In case you don't feel like running the container, here's a sample:

![sample_ui](frontend/assets/sample_ui.png)