<template>
   <div class="initial_load">
      <img src="@/assets/hzi-logo.svg" alt="">
      <div>
        <div class="ball-grid-pulse"><div class="boxes">
    <div class="box">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
    </div>
    <div class="box">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
    </div>
    <div class="box">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
    </div>
    <div class="box">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
    </div>
</div>
</div>
        <h5 class="title initial_load_text">Loading Heatmap</h5>
        <small id="subtitle">v0.0.1-alpha</small>
      </div>
    </div>
</template>

<style>
/* Initializing loader */
#subtitle {
  color: #004085;
}
.ball-grid-pulse {
  height: 148px;
}
.ball-grid-pulse {
  margin: auto;
}
.initial_load {
  /* background-color: #f8f9fa; */
  background-color: #fff;
  color: #007bff;
  width: 100vw;
  height: 100vh;
  position: absolute;
  text-align: center;
  z-index: 1099;
}
.initial_load > * {
  margin: auto;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -50%);
}
.initial_load > img {
  height: 16px;
  top: 3%;
}
.initial_load > div {
  top: 55%
}
.initial_load_text {
  margin-top: 1rem;
  font-weight: 600 !important;
}

/*
Loading animation CSS
*/

.boxes {
  --size: 32px;
  --duration: 800ms;
  margin: auto;
  height: calc(var(--size) * 2);
  width: calc(var(--size) * 3);
  position: relative;
  -webkit-transform-style: preserve-3d;
          transform-style: preserve-3d;
  -webkit-transform-origin: 50% 50%;
          transform-origin: 50% 50%;
  margin-top: calc(var(--size) * 1.5 * -1);
  -webkit-transform: rotateX(60deg) rotateZ(45deg) rotateY(0deg) translateZ(0px);
          transform: rotateX(60deg) rotateZ(45deg) rotateY(0deg) translateZ(0px);
}
.boxes .box {
  width: var(--size);
  height: var(--size);
  top: 0;
  left: 0;
  position: absolute;
  -webkit-transform-style: preserve-3d;
          transform-style: preserve-3d;
}
.boxes .box:nth-child(1) {
  -webkit-transform: translate(100%, 0);
          transform: translate(100%, 0);
  -webkit-animation: box1 var(--duration) ease infinite;
          animation: box1 var(--duration) ease infinite;
}
.boxes .box:nth-child(2) {
  -webkit-transform: translate(0, 100%);
          transform: translate(0, 100%);
  -webkit-animation: box2 var(--duration) ease infinite;
          animation: box2 var(--duration) ease infinite;
}
.boxes .box:nth-child(3) {
  -webkit-transform: translate(100%, 100%);
          transform: translate(100%, 100%);
  -webkit-animation: box3 var(--duration) ease infinite;
          animation: box3 var(--duration) ease infinite;
}
.boxes .box:nth-child(4) {
  -webkit-transform: translate(200%, 0);
          transform: translate(200%, 0);
  -webkit-animation: box4 var(--duration) ease infinite;
          animation: box4 var(--duration) ease infinite;
}
.boxes .box > div {
  --background: #5C8DF6;
  --top: auto;
  --right: auto;
  --bottom: auto;
  --left: auto;
  --translateZ: calc(var(--size) / 2);
  --rotateY: 0deg;
  --rotateX: 0deg;
  position: absolute;
  width: 100%;
  height: 100%;
  background: var(--background);
  top: var(--top);
  right: var(--right);
  bottom: var(--bottom);
  left: var(--left);
  -webkit-transform: rotateY(var(--rotateY)) rotateX(var(--rotateX)) translateZ(var(--translateZ));
          transform: rotateY(var(--rotateY)) rotateX(var(--rotateX)) translateZ(var(--translateZ));
}
.boxes .box > div:nth-child(1) {
  --top: 0;
  --left: 0;
}
.boxes .box > div:nth-child(2) {
  --background: #145af2;
  --right: 0;
  --rotateY: 90deg;
}
.boxes .box > div:nth-child(3) {
  --background: #447cf5;
  --rotateX: -90deg;
}
.boxes .box > div:nth-child(4) {
  --background: #DBE3F4;
  --top: 0;
  --left: 0;
  --translateZ: calc(var(--size) * 3 * -1);
}

@-webkit-keyframes box1 {
  0%,
    50% {
    -webkit-transform: translate(100%, 0);
            transform: translate(100%, 0);
  }
  100% {
    -webkit-transform: translate(200%, 0);
            transform: translate(200%, 0);
  }
}

@keyframes box1 {
  0%,
    50% {
    -webkit-transform: translate(100%, 0);
            transform: translate(100%, 0);
  }
  100% {
    -webkit-transform: translate(200%, 0);
            transform: translate(200%, 0);
  }
}
@-webkit-keyframes box2 {
  0% {
    -webkit-transform: translate(0, 100%);
            transform: translate(0, 100%);
  }
  50% {
    -webkit-transform: translate(0, 0);
            transform: translate(0, 0);
  }
  100% {
    -webkit-transform: translate(100%, 0);
            transform: translate(100%, 0);
  }
}
@keyframes box2 {
  0% {
    -webkit-transform: translate(0, 100%);
            transform: translate(0, 100%);
  }
  50% {
    -webkit-transform: translate(0, 0);
            transform: translate(0, 0);
  }
  100% {
    -webkit-transform: translate(100%, 0);
            transform: translate(100%, 0);
  }
}
@-webkit-keyframes box3 {
  0%,
    50% {
    -webkit-transform: translate(100%, 100%);
            transform: translate(100%, 100%);
  }
  100% {
    -webkit-transform: translate(0, 100%);
            transform: translate(0, 100%);
  }
}
@keyframes box3 {
  0%,
    50% {
    -webkit-transform: translate(100%, 100%);
            transform: translate(100%, 100%);
  }
  100% {
    -webkit-transform: translate(0, 100%);
            transform: translate(0, 100%);
  }
}
@-webkit-keyframes box4 {
  0% {
    -webkit-transform: translate(200%, 0);
            transform: translate(200%, 0);
  }
  50% {
    -webkit-transform: translate(200%, 100%);
            transform: translate(200%, 100%);
  }
  100% {
    -webkit-transform: translate(100%, 100%);
            transform: translate(100%, 100%);
  }
}
@keyframes box4 {
  0% {
    -webkit-transform: translate(200%, 0);
            transform: translate(200%, 0);
  }
  50% {
    -webkit-transform: translate(200%, 100%);
            transform: translate(200%, 100%);
  }
  100% {
    -webkit-transform: translate(100%, 100%);
            transform: translate(100%, 100%);
  }
}
html {
  -webkit-font-smoothing: antialiased;
}

* {
  box-sizing: border-box;
}
*:before, *:after {
  box-sizing: border-box;
}

body {
  height: 100vh;
  color: #ADAFB6;
  display: -webkit-box;
  display: flex;
  -webkit-box-pack: center;
          justify-content: center;
  -webkit-box-align: center;
          align-items: center;
  /* background: #F9FBFF; */
}

</style>
