# CHUM
## CHonk's Unit Modifier

CHUM is a python tool that can help you to add your face to a unit in AoE2:DE. 

**The workflow is a bit convoluted, I know, but unless I get paid I am not reverse engineering the parsing tools into this code base. 
Feel free to do it and leave a MR though ;)**

**SMX based mods still work, but have a lower piority than SLD mods.**

**Steps to add your face to a unit**
1. Select the face you want to add to a unit
    * Avoid any semi-transparent pixels in the image
    * Recommended sprite size ~16-20px
    * If the face is looking into a direction (left or right), create a version that is mirrored
2. Decide what unit you want to add your face to (e.g. elite skirmisher)
3. Select all sprite sheets you want to add your face to 
   * The important files are the _x1.slx, which are used in the regular game. The _x2 are *twice* the size, not sure that they are used for.
   * The location of all units sprite sheets is under
     > [Install path] \Steam\steamapps\common\AoE2DE\resources\_common\drs\graphics\
    * Each unit has several animation sprite sheets, usually, idle, walk, attack etc. 
      For each sprite sheet this process needs to be done individually, e.g. u_arc_eliteskirmisher_walkA_x1.sld
5. Convert *.sld files into *.smx files
   * You can use this website: https://ageofnotes.com/sld-extractor-online-aoe2/
   * if you have a python lib to do that, let me know ;)
4. Export images and masks from smx into the slx file + bmp format
    * e.g. via https://ageofempires.fandom.com/wiki/SLX_Studio
      * In SLX Studio via Graphics/Batch extract SMX to SLX
      * Tip: Create a sub folder first and copy all sprite sheets you want to modify into this subfolder, 
        then run the batch extraction on this subfolder
      * This creates **one** .slx file alongside the images & masks
5. **Modify exported bmps via CHUM**
    * Use chum to modify all images you want and export the modified images & masks
    * Copy the slx file into the output folder together with the modified files
6. Back in the SLX Studio, open the SLX file that you just copied into the folder with the modified sprites.
   This will load the list of all sprites, previewing your modifications.
   * Export it via File/Export (will create smx file). The number of directions seems irrelevant.
7. Create a mod in your game folder from this new SMX file (details see below).


## Getting started with CHUM
You can start the main.py script via `python main.py` (python3 required) or find a Windows executable in the `dist` folder.
(I try to keep the dist folder up to date, but the script is preferred.)
If you start the .exe, make sure that the `imgs` folder is in the same location as the .exe.

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
* You can make parts of a face image transparent (e.g. if the face is hidden behind a relic or barrel) by clicking on the image
in the preview panel.
* Use arrow keys to quickly cycle through the image list

### Export the images
You can export single images or the entire list:
* All images that were opened count as modified (marked as green) even if
  * no face image is used on this image
  * you didn't move the default face image position
* you can right-click on a list entry to remove modifications


### Turn back into SMX file
See description above how to turn the bmp files back into smx via the SLX studio.

### Create a local mod
In order for the changes to show up in the game, you need to create a new mod.
Under the path 
> C:/Users/ [name] / Games /Age of Empires2 DE/ [some huge number] /mods/local

Create a new folder with the name of your mod, e.g. `SkrimsWithMyFace`.
In this folder create three things:
1. The following folder structure: `\SkrimsWithMyFace\resources\_common\drs\graphics`. Then copy all the newly created smx files in there. You need to restart the game to load the new unit sprites.
2. [Optional] A file called `info.json` with the following content:
>{"Author":"Me","CacheStatus":0,"Description":"<p>I changed the Elite skirms.</p>","Title":"SkirmsWithMyFace"}
3. [Optional] an image called "thumbnail.png" that previews your changes
4. [Optional] Create a unit in-game thumbnail (see below)
5. [Optional] Upload mod to the mod workshop
   * https://www.ageofempires.com/mods/create/

### Making an in-game thumbnail
* this it the icon you click on to train the unit or in the selection summary
* There is a colour bug in this, no idea how to fix it - if you know, leave a comment
* Create an icon of the unit ~112px.
* Export as .DDS (e.g. gimp can do that)
* save file as `<Unit-ID>_50730.DDS` in your mod under: `SkirmsWithMyFace\widgetui\textures\ingame\units\`
  * to figure out the unit-ID, you can use the Advanced genie editor
    * https://aok.heavengames.com/blacksmith/showfile.php?fileid=11002