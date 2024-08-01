## Assumptions

- It’s early 2000s, so not the whole world had internet access. In this simplification case, it is assumed that the US is a good estimator for the most basic edition of StorImages.
- At the time, not all modern file types existed, so for now we're gonna just accept JPEGs
- We will consider the approximate number of households that had internet access at the time, based on (very) rough estimations online
- Mind also the internet speed at the time, which pretty sure didn't exceed a few Kbps (kilobits, not a typo)
- Despite the context, we solve with modern tools for an older problem, so this isn't but mere assumptions to have some starting point. Ideally, the system must scale well enough to be useful in the most minimal edition, with nowadays considerations.

### Note
I wanted to iterate locally as much, hence why you see the devcontainer binding to root and the socket mounted. Excuse the abuse of ;, ;;, etc., this is a draft rn.

## Requirements
At the most basic level, the system must be able to resize a picture (generate a thumbnail).
- The system must be able to resize 1 image, several or 1 single zip of images;; further down the road we might add multi-zip options and pic-by-pic selection of thumbnail size
    - both custom valid dimensions and preset
    - Return value is always a zip, including the original picture and the resized options selected from a dropdown menu
    - If only 1 image is resized, it would be nice to have the preview right at the browser
- The system only allows for valid (supported by pillow, picture images) files, so anything else must be excluded
    - When an image is either corrupted, not supported or a given error happens, the original picture is zipped with a note on what happened and only those supported are returned within the zip, or ideally directly output in the GUI
- The user is able to drag and drop a zip from their computer from scratch for comfort
- Ideally
    - loading bar
    - edit backgrounds
    - add watermark
    - customisations

## Concept
- fe = frontend; a dash app
  - bootstrap components
- be = backend; a flask app
  - served with gunicorn
- shared media = to exchange pics and just exchange over requests text

### Flow
1. fe gathers inputs and makes some validations; actually might do some extra work
   1. provided input is right, sends data of picture(s) for processing
2. be processes and sends back data about the picture(s)
3. fe returns a zip with results to user

## Pseudo
### Frontend 
1. Receive 1 zip, 1 image or a selection of images (either drag and drop or opening a file explorer / finder window);; make it easy to upload different types of zip files (tarballs, etc.);; limit batches to 10
    1. Unzip at the frontend
        1. If the unzip fails
            1. Try to fix unzip with -FF
                1. If it fails
                    1. Returns immediately that to the user with the cause (if expected in the local) possible cause
        2. Else, proceed
    2. Check that all the pictures uploaded are a supported picture format
        1. If not
            1. Report back in the output to the user that the file format of a given filename isn’t supported and therefore will be excluded from the result
        2. If they all are supported
            1. Showcase a list to the user of the resources that will be uploaded with an emoji or the likes in the GUI
    4. Allow the user for a single selection of the thumbnail to be generated;; add the dimensions next to the text in parentheses;; add an option to customize dimensions
        1. Photo galleries = 120x90 pixels
        2. Video = 160x120 pixels
        3. Social media profile picture = 100x100 pixels
        4. Online store - small = 80x80 pixels
        5. Online store - large = 150x150 pixels
        6. Icons = 96x96 pixels
2. Make the user confirm the selection to be submitted is right; submit button must be blocked while the process is loading and a load bar should appear
    1. If user submits
        1. Hash each original image in the frontend;; we'd hash so if a pic is uploaded twice w/ diff names, it's not reprocessed & other purposes; kinda memoizing, not needed at start (early optimization is the root of all evil, Ik) but might come in handy for high res, big bunches or the odd chance 2 diff users upload the same pic
            1. Create a JSON to map the original names to their hashes
                1. If the hashed original picture is stored already
                    1. Check JSON index or any other medium to see if dimension selected is stored in shared volume
                        1. If it exists
                            1. Copy it at the frontend into the final zip
                            2. Skip the request
                        2. If it does not exist 
                            1. Send the request
                    2. Exclude that from the requests to be sent, but retrieve it from the volume and copy it into the request’s dir-to-be-zipped
                            1. Make sure to normalize the name of the directory to replace spaces by underscores and all lowercase
                2. If the hash does not exist and picture isn’t yet stored
                    1. Save the hash-name relationship to JSON
                    2. Proceed
    2. If user refreshes or cancels (add a clear button)
        1. Clear the GUI
        2. Delete the uncompressed directory and zip
3. Send the requests to the respective backend service
    1. Send the hash of the original picture to the resizing service asynchronously
    2. Gather the responses 
        1. If error
            1. Continue and create a document of missing compressed files;; or output to screen; doc would be better so user doesn't miss out / transparency
        2. Else
            1. Copy the files from the shared volume into the new dir; same name as original but ends in _thumbnails. Name is normalized
    3. Gather actual pics into the dir
    4. Zip the dir
    5. Make it downloadable

### Backend
1. Receives a single request, including:
    1. Hash (name) of the original picture
    2. Includes the dimensions for resizing
2. Resizes the picture
    1. If fails
        1. Returns
            1. error message
            2. Dimensions
            3. Original hash
    2. If succeeds, returns
        1. Hash of new picture
        2. Hash of the og picture
3. Stores the picture with same hash appending new resolution at the end

## Components
1. fe
  1. Upload area
      1. Drag and drop
         1. Click to file select
      2. Submit button
  2. Showcases (non interactive at first) like a preview of what was uploaded; make the user sure
  3. Callback functions (for actual interactivity)
  4. Aesthetics & UX
2. be
  1. Flask endpoint
  2. Gunicorn
3. Infra, etc.
   1. ECS & image registry = well, for running both fe and be
   1. ALB = or the likes, at the center of requests entropy
   2. Terraform and handy scripts
   3. Monitoring and analytics: big plus to understand usage and focus dev factually

<!-- ## Structure

- docs/
    - Diagram
- *.sh
    - Script to rebuild everything from scratch
- tests/
  - might not be viable rn but desirably
- Repository with README.md
    - Build the app locally
    - How to deploy, etc.
    - Core features of the iteration
 -->
