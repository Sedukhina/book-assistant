export const modelViewer = document.querySelector('#myModel');

modelViewer.addEventListener('load', () => {
  modelViewer.timeScale = 0.5; // Adjust this value to control speed
});


export const ANIMATIONS = [
  'Bounce',
  'Eat',
  'Idle_A',
  'Roll',
  'Run',
  'Sit',
  'Spin',
  'Walk'
]

export const setAnimation = (animation) => {
  modelViewer.animationName = animation;
}

export const listenAnimation = () => {
  modelViewer.animationName = 'Idle_A';
}

export const waitAnimation = () => {
  modelViewer.animationName = 'Eat';
}

export const speakingAnimation = () => {
  modelViewer.animationName = 'Run';
}