.. _example_mainmenu:



Simple Main Menu Example
=====================================

.. code-block::
    :linenos:

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


.. image:: ../_static/my_images/Pygame\ GUI\ XML\ Main\ Menu\ Example.png
    :width: 800
    :height: 600
    :alt: An example showing 3 bars of text, the top bar saying Main Menu, the middle bar saying "Enter the Game", and the bottom bar with 3 buttons which say "Play", "Options", and "Quit" respectively