# Ray-caster

This is a Ray-caster coded in python composed of:
- a level editor
- a top/bird view
- an FPS view window

## Usage

1. Clone the repository 
```
git clone https://github.com/wragle/ray-caster.git
```

2. Go into the folder you just cloned
```
cd ray-caster
```

3. Run the python program
```
python3 RAYCASTER\ 2.py
```

You might encounter problems depending on your python envrionment and the packages you already have installed.

If you get the error message "Python may not be configured for Tk", have a look at the following StackOverflow post [here](https://stackoverflow.com/questions/5459444/tkinter-python-may-not-be-configured-for-tk).

## Controls

If you are reading this, that means you executed the program successfully. Congrats ! 🎉

Controls are:
- **W-A-S-D** to move
- **O-P** to turn camera

You can also build your own level on the level editor by clicking the grid buttons like show in the picture below:

![LevelEditor picture](/images/levelEditor.png)

Your field of view and your position on the 2D map will be shown to you in the bird view window like show below:

![BirdView picture](/images/birdView.png)

## Settings

FPS, FOV, ray_count can all be changed to your desired result

having enable_bird = True will open a window that shows a top down view of the rays and collisions

having enable_editor = True will have a window open that shows the level from a top down view, clicking in squares will toggle them from wall to empty, you can also change the size of the level
