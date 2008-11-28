<?xml version="1.0" encoding="UTF-8"?>

<!--
  Copyright (C) 2008 Carlos III University of Madrid
  This file is part of the ADA: Agile Distributed Authoring Toolkit

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor
  Boston, MA  02110-1301, USA.

-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:exsl="http://exslt.org/common" 
  xmlns="http://www.w3.org/1999/xhtml" version="1.0">

  <!-- Show the solutions -->
  <xsl:param name="ada.testquestions.include.solutions" select="'no'"/>

  <!-- Show the qandadiv ID -->
  <xsl:param name="ada.testquestions.include.id" select="'no'"/>

  <!-- Insert history remarks -->
  <xsl:param name="ada.testquestions.include.history" select="'no'"/>

  <!-- Insert pagebreaks as specified in the sectioninfo -->
  <xsl:param name="ada.testquestions.insert.pagebreaks" select="'yes'"/>

  <!-- Render one question per page -->
  <xsl:param name="ada.testquestions.render.onequestionperpage" select="'no'"/>

  <!-- Size of the square to mark -->
  <xsl:param name="ada.testquestions.render.squaresize" select="'10pt'"/>

</xsl:stylesheet>
