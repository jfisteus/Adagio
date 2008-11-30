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
  xmlns="http://www.w3.org/1999/xhtml" 
  exclude-result-prefixes="exsl" version="1.0">
  
  <!-- Include the solutions for the exercises --> 
  <xsl:param name="solutions.include.guide" select="'no'"
    description="yes/no variable to show the solution in the document"/>

  <!-- Conditionally process section TOC -->
  <xsl:template match="section[@condition = 'solution']" mode="toc">
    <xsl:param name="toc-context" select="."/>
    <xsl:if test="$solutions.include.guide = 'yes'">
      
      <xsl:call-template name="subtoc">
        <xsl:with-param name="toc-context" select="$toc-context"/>
        <xsl:with-param name="nodes" 
          select="section|bridgehead[$bridgehead.in.toc != 0]"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>
  
  <!-- Conditionally process section when chunked -->
  <xsl:template match="section[@condition = 'solution']">
    <xsl:if test="$solutions.include.guide = 'yes'">
      <xsl:variable name="depth" select="count(ancestor::section)+1"/>
      
      <xsl:call-template name="id.warning"/>
      
      <div>
        <xsl:apply-templates select="." mode="class.attribute"/>
        <xsl:call-template name="dir">
          <xsl:with-param name="inherit" select="1"/>
        </xsl:call-template>
        <xsl:call-template name="language.attribute"/>
        <xsl:call-template name="section.titlepage"/>
        
        <xsl:variable name="toc.params">
          <xsl:call-template name="find.path.params">
            <xsl:with-param name="table" select="normalize-space($generate.toc)"/>
          </xsl:call-template>
        </xsl:variable>
        
        <xsl:if test="contains($toc.params, 'toc')
                      and $depth &lt;= $generate.section.toc.level">
          <xsl:call-template name="section.toc">
            <xsl:with-param name="toc.title.p" 
              select="contains($toc.params, 'title')"/>
          </xsl:call-template>
          <xsl:call-template name="section.toc.separator"/>
        </xsl:if>
        <xsl:apply-templates/>
        <xsl:call-template name="process.chunk.footnotes"/>
      </div>
    </xsl:if>
  </xsl:template>

  <!-- Process the section labeled with condition=solution -->
  <xsl:template match="note[@condition='solution']">
    <xsl:if test="$solutions.include.guide = 'yes'">
      <table class="ada_solution_table">
        <tr>
          <td><xsl:call-template name="nongraphical.admonition"/></td>
        </tr>
      </table>
    </xsl:if>
  </xsl:template>

  <!-- Process the section labeled with condition=solution -->
  <xsl:template match="phrase[@condition='solution']">
    <xsl:if test="$solutions.include.guide = 'yes'">
      <b>
        <xsl:choose>
          <xsl:when test="$profile.lang='es'">Solucion:</xsl:when>
          <xsl:otherwise>Solution:</xsl:otherwise>
        </xsl:choose>
      </b>
      <xsl:apply-templates />
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>
