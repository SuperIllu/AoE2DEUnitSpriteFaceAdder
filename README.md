# CHUM
## CHon's Unit Modifier

CHUM is a python tool that can help you to add your face to a unit in AoE2:DE. 

**Steps to add your face to a unit**
1. Select the face you want to add to a unit
    * Avoid any semi-transparent pixels in the image
    * Recommended sprite size ~16-20px
    * If the face is looking into a direction (left or right), create a version that is mirrored
2. Decide what unit you want to add your face to (e.g. elite skirmisher)
3. Select all sprite sheets you want to add your face to (e.g. u_arc_eliteskirmisher_walkA_x1.smx)
    * Each unit has several animation sprite sheets, usually, idle, walk, attack etc.
4. Export images and masks from smx into the slx file + bmp format
    * e.g. via https://ageofempires.fandom.com/wiki/SLX_Studio
5. **Modify exported bmps via CHUM**
    * Copy the slx file into the output folder together with the mofidied files
6. Import this slx file back into SLX studio and export (will create smx file)
7. Create a mod in your game folder


## Getting started with CHUM
Start the .exe, but make sure that the `imgs` folder is in the same location as the .exe.
Select the input folder that contains the exported bmps.
Select all face pictures to be overlaid over the unit sprites.
Select the output folder, I recommend a new, empy one.
Click the load button, this will perform some rudimentary checks.

### Modify the images
Select the image in the list you want to work on. 
Select which image (face) you want to overlay over the unit sprite.
Position the face over the unit's face:
* either click the buttons to move
* put in a value directly into the textbox
* use WASD keys to move the face

### Export the images
You can export single images or the entire list:
* All images that were opened count as modified, even if you didn't move the default face image position

### Create a local mod
In order for the changes to show up in the game, you need to create a new mod.
Under the path 
> C:/Users/<name>/Age of Empires2 DE/<some huge number>/mods/local

Create a new folder with the name of your mod, e.g. `SkrimsWithMyFace`.
In this folder create three things:
1. The following folder structure: `\EllieteSkirms\resources\_common\drs\graphics`. Then copy all the newly create smx files in there. You need to restart the game to load the new unit sprites.
2. [Optional] A file called `info.json` with the following content:
>{"Author":"Me","CacheStatus":0,"Description":"<p>I changed the Elite skirms.</p>","Title":"SkirmsWithMyFace"}
3. [Optional] an image called "thumbnail.png" that previews your changes
