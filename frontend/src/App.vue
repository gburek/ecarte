<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
    export const AJAX_END = 'AjaxEnd'

    export default {
        name: 'App'
    }
</script>

<style lang="scss">
    html {
        height: 100%;
    }

    body {
        padding: 0;
        margin: 0;
        background-color: black;
        background-image: url('/static/img/taco.jpg');
        background-repeat: repeat-y;
        background-size: 100%;
    }
</style>
