<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exsl="http://exslt.org/common"
  xmlns:str="http://exslt.org/strings"
  xmlns:xi="http://www.w3.org/2001/XInclude"
  version="1.0" exclude-result-prefixes="exsl str xi">
  
  <xsl:import href="BasicFunctions.xsl"/>
  <xsl:strip-space elements="*"/>

  <xsl:preserve-space elements="xsl:text"/>
   
  <xsl:output method="text" encoding="UTF-8" indent="no"/>
  
  <xsl:template match="/projects">#
# List of properties to include in the file Properties.txt
#
#
# The values that appear next to the equal sign are the default values. You 
# only need to include a new definition if it is different from the default 
# value.
#
# Whenever a list of files is required, unless otherswise noted, it is a comma
# or space separated of filenames (no paths).
#
# The value ${basedir} refers to the same location where the Properties.txt 
# file is.
#
# The variables ada.home and ada.course.home are defined respectively to the
# directory where ADA is installed, and the parent directory of the current
# one where the file AdaCourseParams.xml has been found (if any).
<xsl:apply-templates select="project"/>
  </xsl:template>

  <xsl:template match="project">
    <xsl:if test="description">
      <xsl:variable name="repl1"><xsl:call-template name="str:replace">
      <xsl:with-param name="string" select="description/text()"/>
      <xsl:with-param name="search" select="'&#10;'"/>
      <xsl:with-param name="replace" select="'&#10;#'"/></xsl:call-template></xsl:variable>
      <xsl:variable name="repl2"><xsl:call-template name="str:replace">
      <xsl:with-param name="string" select="$repl1"/>
      <xsl:with-param name="search" select="'#  '"/>
      <xsl:with-param name="replace" select="'#'"/></xsl:call-template></xsl:variable>
###########################################################################
# -<xsl:value-of select="$repl2"/>-
<!--
# <xsl:value-of select="str:replace(str:replace(description/text(), '&#10;', 
      '&#10;#'), '#  ', '#')" />
-->
###########################################################################</xsl:if>
    <xsl:for-each select="descendant::property[@description != '']">
# <xsl:value-of select="@description"/>
# <xsl:value-of select="@name"/>=<xsl:value-of select="@value"/><xsl:text>
</xsl:text>
  </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>
