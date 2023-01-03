# Pygame GUI XML

An W.I.P highly experimental XML Syntax and parser for writing GUI applications with the [pygame_gui](https://github.com/MyreMylar/pygame_gui) library for pygame applications

Example Output:

![Main Menu Screen](screenshots/Pygame%20GUI%20XML%20Main%20Menu%20Example.png)

Markup:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE pygamegui>

<pygamegui> 
    <head>
        <themes>
            <theme>styles.json</theme>
        </themes>
    </head>

    <body>
        <panel rect="0 0 800 600" id="background">
            <panel rect="20 20 760 200" id="top-bar">
                <label rect="20 20 700 160">Main Menu</label>
            </panel>

            <panel rect="20 200 760 200" id="middle-bar">
                <label rect="20 20 700 160">Enter the Game</label>
            </panel>

            <panel rect="20 -220 760 200" anchors="bottom" id="bottom-bar">
                <button rect="100 0 150 100" anchors="centery" id="play-button" tooltip="Start New Game">Play</button>
                <button rect="300 0 150 100" anchors="centery" id="options-button">Options</button>
                <button rect="500 0 150 100" anchors="centery" id="quit-button">Quit</button>
            </panel>
        </panel>
    </body>

</pygamegui>
```

Dependencies: bs4, pygame, pygame_gui
Docs Dependencies: sphinx_pdj_theme, sphinx
