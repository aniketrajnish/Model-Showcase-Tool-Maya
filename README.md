# Model Showcase Tool Maya
 * A tool that creates a camera animation around your model to display it professionally.
 * The camera is keyframed at 45 degree intervals and the tool adjusts the camera position to accommodate the size of model and reference images.
 * The display mode is alternated between wireframe and smooth shading and both modes are displayed for each angle.

 ## Usage
 ### How to Load
 * Clone the repository or download the script from [here](https://github.com/aniketrajnish/Model-Showcase-Tool-Maya/blob/main/src/showcase.py).
    ```
    git clone https://github.com/aniketrajnish/Alembic-to-FBX-File-Maya.git
    ```  
 * Open Script Editor in Maya.
 * Go to `File -> Open Script` and select the python script from the repository (`src/showcase.py`)
 * Click on Play Button.
 * You can create a shortcut for the tool by copying all its content from the script editor and middle mouse dragging it to a shelf.

https://github.com/aniketrajnish/Model-Showcase-Tool-Maya/assets/58925008/f14c9e8b-ded9-408a-8158-9b59d386f936

### How to Run
* The tool has the following options:
  
 | Parameter       | Description                                                                |
 |-----------------|----------------------------------------------------------------------------|
 | **Model**       | Dropdown to select the 3D model for showcasing.                            |
 | **Reference 0** | Optional: Dropdown to select the reference image at 0 degrees.             |
 | **Reference 90**| Optional: Dropdown to select the reference image at 90 degrees.            |
 | **Reference 270**| Optional: Dropdown to select the reference image at 270 degrees.          |
 | **Camera Distance** | Slider to adjust the camera's distance from the model.                 |
 | **Camera Pitch**    | Slider to adjust the camera's pitch angle around the model.            |

* Choose your model and reference images (optional).
* Adjust the camera distance and pitch (angle) according to your needs.
* Click on Showcase.

https://github.com/aniketrajnish/Model-Showcase-Tool-Maya/assets/58925008/a34f915f-de7f-4c81-931a-5e9b8b642f10

## Contribution
Contributions to the project are welcome. Currently working on:
* Toggling Display Mode when animation is playing.
* Toggling the Display Mode Toggle.

## License
MIT License
