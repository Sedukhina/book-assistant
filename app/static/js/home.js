import { setAnimation, ANIMATIONS, modelViewer } from "./3dModel.js";


const buttonContainer = document.createElement('div');
buttonContainer.classList.add('animation-buttons');

ANIMATIONS.forEach(animation => {
  const button = document.createElement('button');
  button.textContent = animation;
  button.addEventListener('click', () => {
    setAnimation(animation);
    const currentOrbit = modelViewer.getCameraOrbit();
    console.log("Current Camera Orbit:", currentOrbit.toString());
  });
  buttonContainer.appendChild(button);
})

document.body.appendChild(buttonContainer);