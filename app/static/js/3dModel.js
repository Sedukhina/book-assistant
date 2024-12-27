export const modelViewer = document.querySelector('#myModel');

modelViewer.addEventListener('load', () => {
    modelViewer.timeScale = 0.5; // Adjust this value to control speed
    modelViewer.animationName = 'Idle_A'; // Set default animation
    console.log('Model loaded, animation set to Idle_A');
});


// export const ANIMATIONS = [
//   'Bounce',
//   'Eat',
//   'Idle_A',
//   'Roll',
//   'Run',
//   'Sit',
//   'Spin',
//   'Walk'
// ]

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
