# backend/
The backend/ directory has the contents to serve the thumbnail generator as a HTTP endpoint.

## Build
### Note: 
The latest build is available in my public repository for this challenge. All builds are derived from my private **morezio/envs:u_dev**, which is based on **ubuntu:jammy**, adding commodities for development (ohmyzsh, auto-suggestions, poetry, docker client [to mount the socket], etc.) as seen in the history of the layers.
```zsh

# Make sure to be located at /storimages 
docker build -t <your-repository>/storimages:be -f backend.dockerfile .
```
## Pull
Latest build is online!
```zsh
docker pull morezio/storimages:be
```
## Try it!
First you need to create an instance of the image like:
```zsh
# The image comes with a wikimedia commons cat to be used resized, not committed because
# it is online and is just an example 
docker run -d -p 80:80 --name be morezio/storimages:be

# I advise you to test it out with whatever picture you want to bind the directory on your machine
# into any directory within /storimages
docker run -v /home/user/cats_pictures:/storimages/backend -d -p 80:80 --name be morezio/storimages:be

```
Then, listening on port 80, you can send a request with **curl** like:
```zsh
# Note how I send the dimensions as an array, but else, you preferably should send a tuple
# Python requests can take care of that

curl -X POST http://0.0.0.0:80/create_thumbnail -H "Content-Type: application/json" -d '{"filename":"/storimages/backend/Cat03_1600x1598.jpg", "dimensions":[100,100]}'
```
Any requests issued to the endpoint have to **POST** the data into the body of the request like:
```json
{
    "filename": "/storimages/backend/Cat03_1600x1598.jpg",
    "dimensions": [
        100,
        100
    ]
}
```
1. **filename** = the absolute path (within /storimages) to the picture you want to resize
2. **dimensions** = W x L for the thumbnail

The request above will return:
- **filename** = the absolute path (within the container) where your resized cat can be found
- **request** = the params you sent
```json
{
    "filename": "/storimages/backend/Cat03_1600x1598_100x100.jpg",
    "request": {
        "dimensions": [
            100,
            100
        ],
        "filename": "/storimages/backend/Cat03_1600x1598.jpg"
    }
}
```
Yeah, I know you spotted some things like ~~**filename** repeated in the request and response~~ the fandom for mixing cats with computers but there's more to it in the source code.

I tried to prioritise readability within the source code, although I cluttered with some notes to self here and there. No docstrings yet and didn't use hinted the internal methods. Not that I wrote a newspaper but I appreciate when others care to make their code easy to follow, so, sorry if this is unmet.

I use some extensions that work like a charm:
- For reviewing branches, commits, etc. visually. Can come in handy if you didn't know it already:

Name: Git Graph
<br>
Id: mhutchie.git-graph
<br>
Description: View a Git Graph of your repository, and perform Git actions from the graph.
<br>
Version: 1.30.0
<br>
Publisher: mhutchie
<br>
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph
<br>

- For Markdown stuff:

Name: Markdown All in One
<br>
Id: yzhang.markdown-all-in-one
<br>
Description: All you need to write Markdown (keyboard shortcuts, table of contents, auto preview and more)
<br>
Version: 3.6.2
<br>
Publisher: Yu Zhang
<br>
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one