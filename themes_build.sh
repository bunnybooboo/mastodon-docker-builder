#!/bin/sh

THEMES="./themes/"
PUBLIC="./themes_public/"

mkdir -p $THEMES $PUBLIC

cp themes_src/witches-town-theme/witches-town.scss $THEMES
cp -r themes_src/witches-town-theme/witchesAwesome $PUBLIC
