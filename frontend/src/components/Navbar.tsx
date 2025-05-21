import React from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton } from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <IconButton edge="start" color="inherit" aria-label="menu">
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" style={{ flexGrow: 1 }}>
          TRAINSET
        </Typography>
        <Button color="inherit">Home</Button>
        <Button color="inherit">Help</Button>
        <Button color="inherit">Labeler</Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
