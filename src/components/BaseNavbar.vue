<template>
  <nav class="navbar navbar-expand-lg fixed-top">
    <slot name="nav-content">
      <h1 class="navbar-brand"><router-link class="homeLink" v-bind:to="'/'">TRAINSET<img id="logo" src="/static/trainset_logo.png" style="width:100px;height:auto;"></router-link></h1>
      <div class="navbar-nav ml-auto">
        <router-link class="nav-link" v-bind:to="'/help'">Help</router-link>
        <router-link class="nav-link" v-bind:to="'/license'">License</router-link>
        <router-link class="nav-link" v-bind:to="'/timeline'">Demo</router-link>
        <router-link class="nav-link" v-bind:to="'/analytics'">Analytics</router-link>
        <router-link class="nav-link" v-bind:to="'/project-management'">Manage Data</router-link>
        <router-link class="nav-link" v-bind:to="'/explore'">Explore</router-link>

  display: inline-block;
  position: static;
      </div>
    </slot>
  </nav>
</template>

<script>
export default {
  name: "BaseNavbar"
};
</script>

<style scoped>
.navbar { background:#7E4C64; }
>>> .nav-link , .navbar-brand { color: #f4f4f4; cursor: pointer; }
.nav-link { margin-right: 1em !important; }
.nav-link:hover { background: #f4f4f4; color: #7E4C64; }
.navbar-toggler { background:#fff !important; }
.navbar-nav { float: right; }
.homeLink { text-decoration: none; color: inherit; }
.homeLink:hover { text-decoration: none; color: inherit; }
>>> #logo {
  width: 100px;
  height: auto;
  max-height: none;
}
</style>