export const modelViewer = document.querySelector('#myModel');

modelViewer.addEventListener('load', () => {
    modelViewer.timeScale = 0.5; // Adjust this value to control speed
    modelViewer.animationName = 'Idle_A'; // Set default animation
});

export const setAnimation = (animation) => {
  modelViewer.animationName = animation;
}

export const listenAnimation = () => {
  modelViewer.animationName = 'Spin';
}

export const waitAnimation = () => {
  modelViewer.animationName = 'Idle_A';
}

export const speakingAnimation = () => {
  modelViewer.animationName = 'Eat';
}
