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
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:exsl="http://exslt.org/common"
  xmlns:str="http://exslt.org/strings"
  xmlns:xi="http://www.w3.org/2001/XInclude"
  version="1.0" exclude-result-prefixes="exsl str xi">

  <!-- Brings in all the default values -->
  <xsl:import href="HeadTailParams.xsl"/>

  <xsl:import href="RssParams.xsl"/>

  <xsl:import href="DocbookProfile.xsl"/>

  <xsl:import href="DublinCore.xsl"/>

  <!-- Template to manipulate CSSs -->
  <xsl:import href="CSSLinks.xsl"/>

  <!-- Template to ignore the chapter/section info with rss.info condition -->
  <xsl:import href="RssIgnore.xsl"/>

  <!-- Invoke the templates to process professor guide and solution -->
  <xsl:import href="PguideSection.xsl"/>
  <xsl:import href="SolutionSection.xsl"/>

  <xsl:output method="xml" indent="yes" encoding="UTF-8"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
    doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/>

  <!-- Docbook XSL parameters needed generate strict XHTML -->
  <xsl:param name="css.decoration">0</xsl:param>
  <xsl:param name="html.longdesc">0</xsl:param>
  <xsl:param name="ulink.target" />
  <xsl:param name="use.viewport">0</xsl:param>
  <xsl:param name="generate.id.attributes">1</xsl:param>

  <!-- Propagate the role attribute as class element when allowed -->
  <xsl:param name="emphasis.propagates.style">1</xsl:param>
  <xsl:param name="entry.propagates.style">1</xsl:param>
  <xsl:param name="para.propagates.style">1</xsl:param>
  <xsl:param name="phrase.propagates.style">1</xsl:param>

  <!-- This one for sure is needed in all documents -->
  <xsl:param name="xref.with.number.and.title" select="'0'"/>

  <!-- Template processing the root. Need to overwrite to include div elements -->
  <xsl:template match="*" mode="process.root">
    <xsl:variable name="doc" select="self::*"/>

    <xsl:call-template name="user.preroot"/>
    <xsl:call-template name="root.messages"/>

    <html>
      <xsl:call-template name="language.attribute"/>
      <head>
        <xsl:call-template name="system.head.content">
          <xsl:with-param name="node" select="$doc"/>
        </xsl:call-template>
        <xsl:call-template name="head.content">
          <xsl:with-param name="node" select="$doc"/>
        </xsl:call-template>
        <xsl:call-template name="user.head.content">
          <xsl:with-param name="node" select="$doc"/>
        </xsl:call-template>
      </head>

      <body>

        <xsl:call-template name="body.attributes"/>

        <div id="ada_body_container">

          <xsl:call-template name="ada_page_header_content">
            <xsl:with-param name="node" select="$doc"/>
          </xsl:call-template>

          <div id="ada_page_content">
            <a name="ada_page_content_anchor"/>
            <xsl:apply-templates select="."/>
          </div>

          <div id="ada_page_footer">
            <xsl:call-template name="user.footer.content">
              <xsl:with-param name="node" select="$doc"/>
            </xsl:call-template>
          </div>
        </div>
      </body>
    </html>
    <xsl:value-of select="$html.append"/>
  </xsl:template>

  <xsl:template name="body.attributes">
    <xsl:variable name="default_status">
      <xsl:apply-templates
        select="/" mode="object.title.markup.textonly"/>
    </xsl:variable>

    <!-- Insert the onload attribute with the window.defaultStatus value -->
    <!-- www.webaim.org says this is a problem, so ignore it!
    <xsl:if test="$default_status and $default_status != ''">
      <xsl:attribute name="onload">window.defaultStatus='<xsl:value-of
      select="$default_status"/>';</xsl:attribute>
    </xsl:if>
    -->

    <!-- Copy the id attribute from the root element -->
    <xsl:if test="/*[@id] and /*[@id] != ''">
      <xsl:attribute name="id">adaroot_<xsl:value-of select="/*/@id"/></xsl:attribute>
    </xsl:if>
  </xsl:template>

  <!-- User HEAD content -->
  <xsl:template name="user.head.content">

    <!-- Insert Dublin Core Metadata -->
    <xsl:call-template name="ada.dc.insert.meta.elements"/>

    <!-- Javascripts -->
    <xsl:if test="$ada.head.javascripts">
      <xsl:copy-of select="$ada.head.javascripts"/>
    </xsl:if>

    <!-- FAVICON -->
    <xsl:if test="$ada.project.icon">
      <link rel="shortcut icon">
        <xsl:attribute name="href"><xsl:value-of
        select="$ada.project.home"/><xsl:value-of
        select="$ada.project.icon"/></xsl:attribute>
        <xsl:attribute name="type"><xsl:value-of
        select="$ada.project.icon.type"/></xsl:attribute>
      </link>
      <link rel="icon">
        <xsl:attribute name="href"><xsl:value-of
        select="$ada.project.home"/><xsl:value-of
        select="$ada.project.icon"/></xsl:attribute>
        <xsl:attribute name="type"><xsl:value-of
        select="$ada.project.icon.type"/></xsl:attribute>
      </link>
    </xsl:if>

    <!-- Author Meta Element -->
    <xsl:variable name="author_string">
      <xsl:choose>
        <xsl:when test="/*/*/author">
          <xsl:call-template name="person.name"/>
        </xsl:when>
        <xsl:when test="/*/*/authorgroup">
          <xsl:call-template name="person.name.list">
            <xsl:with-param name="person.list"
              select="/*/*/authorgroup/author"/>
          </xsl:call-template>
        </xsl:when>
        <xsl:when test="$ada.page.author">
          <xsl:value-of select="$ada.page.author"/>
        </xsl:when>
      </xsl:choose>
    </xsl:variable>

    <xsl:if test="$author_string and $author_string != ''">
      <xsl:element name="meta">
        <xsl:attribute name="name">Author</xsl:attribute>
        <xsl:attribute name="content">
          <xsl:value-of select="string($author_string)"/>
        </xsl:attribute>
      </xsl:element>
    </xsl:if>

    <xsl:element name="meta">
      <xsl:attribute name="name">language</xsl:attribute>
      <xsl:attribute name="content">
        <xsl:choose>
          <xsl:when test="$profile.lang and $profile.lang != ''">
            <xsl:value-of select="$profile.lang"/>
          </xsl:when>
          <xsl:otherwise>en</xsl:otherwise>
        </xsl:choose>
      </xsl:attribute>
    </xsl:element>

    <!-- Stick the javascript for the flash player -->
    <xsl:if test="$ada.flv.player.js.file and ($ada.flv.player.js.file != '')
                  and /*/para[@condition = 'ada.flv.player']">
      <script type="text/javascript" language="JavaScript">
        <xsl:attribute name="src"><xsl:value-of
        select="$ada.flv.player.js.file"/></xsl:attribute>
      </script>
    </xsl:if>

    <!-- If refresh rate has been given, include it -->
    <xsl:if test="$ada.page.refresh.rate and ($ada.page.refresh.rate != '')">
      <meta http-equiv="refresh">
        <xsl:attribute name="content"><xsl:value-of
        select="$ada.page.refresh.rate"/></xsl:attribute>
      </meta>
    </xsl:if>

    <!-- CSS styles -->
    <xsl:if test="$ada.page.cssstyle.url">
      <xsl:call-template name="ada_link_rel_css">
        <xsl:with-param name="node" select="$ada.page.cssstyle.url"/>
      </xsl:call-template>
    </xsl:if>
    <xsl:if test="$ada.page.cssstyle.alternate.url">
      <xsl:call-template name="ada_link_rel_css">
        <xsl:with-param name="node" select="$ada.page.cssstyle.alternate.url"/>
        <xsl:with-param name="rel" select="'alternate stylesheet'"/>
      </xsl:call-template>
    </xsl:if>


    <!-- FIXME: Instead of the link element, include code similar to:
         <style type="text/css" media="MMMM">@import "blah.css";</style>
         -->

    <!-- Insert the reference to the RSS channel if given -->
    <xsl:if test="$ada.rss.channel.url and ($ada.rss.channel.url != '')">
      <link rel="alternate" type="application/rss+xml" title="rss">
        <xsl:attribute name="href"><xsl:value-of
        select="$ada.rss.channel.url"/></xsl:attribute>
      </link>
    </xsl:if>
  </xsl:template>

  <xsl:template name="ada_page_header_content">
    <xsl:param name="node" select="."/>

    <!-- HIDDEN ELEMENTS -->
    <div class="ada_hidden_elements" id="skip_links">
      <ul>
        <li>
          <a>
            <xsl:attribute name="href"><xsl:value-of
            select="normalize-space($ada.project.home)"/></xsl:attribute>
            <xsl:attribute name="accesskey"><xsl:value-of
            select="$ada.page.navigation.home.accesskey"/></xsl:attribute>
            <xsl:choose>
              <xsl:when test="$profile.lang='es'">Inicio</xsl:when>
              <xsl:otherwise>Home</xsl:otherwise>
            </xsl:choose>
          </a>
        </li>
        <li>
          <a href="#ada_page_content">
            <xsl:attribute name="accesskey"><xsl:value-of
            select="$ada.page.navigation.content.accesskey"/></xsl:attribute>
            <xsl:choose>
              <xsl:when test="$profile.lang='es'">Ir a contenido</xsl:when>
              <xsl:otherwise>Skip to content</xsl:otherwise>
            </xsl:choose>
          </a>
        </li>
        <xsl:if test="$ada.page.navigation and
                      $ada.page.navigation != ''">
          <li>
            <a href="#ada_navigation">
              <xsl:attribute name="accesskey"><xsl:value-of
              select="$ada.page.navigation.navigation.accesskey"/></xsl:attribute>
              <xsl:choose>
                <xsl:when test="$profile.lang='es'">Ir a navegación</xsl:when>
                <xsl:otherwise>Skip to navigation</xsl:otherwise>
              </xsl:choose>
            </a>
          </li>
        </xsl:if>
      </ul>
    </div> <!-- End of ada_hidden_elements -->

    <!-- ADA PAGE HEADER LEVEL1 -->
    <xsl:if test="$ada.page.header.level1">
      <div id="ada_page_header_level1">
        <xsl:copy-of select="$ada.page.header.level1"/>
      </div>
    </xsl:if>

    <!-- ADA PAGE HEADER LEVEL2 -->
    <xsl:if test="$ada.page.header.level2">
      <div id="ada_page_header_level2">
        <xsl:copy-of select="$ada.page.header.level2"/>
      </div>
    </xsl:if>

    <!-- ADA PAGE HEADER LEVEL3 -->
    <xsl:if test="$ada.page.header.level3">
      <div id="ada_page_header_level3">
        <xsl:copy-of select="$ada.page.header.level3"/>
      </div>
    </xsl:if>

    <!-- ADA PAGE HEADER LEVEL4 -->
    <xsl:if test="$ada.page.header.level4">
      <div id="ada_page_header_level4">
        <xsl:copy-of select="$ada.page.header.level4"/>
      </div>
    </xsl:if>

    <!-- ADA.PAGE.NAVIGATION -->
    <xsl:if test="$ada.page.navigation and
                  $ada.page.navigation != ''">
      <div id="ada_page_navigation">
        <a name="ada_navigation"/>
        <xsl:copy-of select="$ada.page.navigation"/>
      </div> <!-- End of ada.page.navigation -->
    </xsl:if>

  </xsl:template>

  <!-- Footer-->
  <xsl:template name="user.footer.content">
    <xsl:if test="$ada.page.footer and $ada.page.footer != ''">
      <xsl:copy-of select="$ada.page.footer" />
    </xsl:if>

    <!-- Insert Google Analytics snippet -->
    <xsl:if test="$ada.page.google.analytics.account">
      <script type="text/javascript">
        var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
        document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
      </script>
      <script type="text/javascript">
        var pageTracker = _gat._getTracker("<xsl:value-of select="$ada.page.google.analytics.account"/>");
        pageTracker._trackPageview();
      </script>
    </xsl:if>
  </xsl:template>

  <xsl:template name="ggadgetlink">
    <xsl:if test="$ada.page.google.gadget.url">
      <a>
        <xsl:attribute
          name="href">http://fusion.google.com/add?moduleurl=<xsl:value-of
        select="$ada.page.google.gadget.url"/></xsl:attribute>
        <img
          src="http://buttons.googlesyndication.com/fusion/add.gif">
          <xsl:attribute name="alt"><xsl:choose>
            <xsl:when
              test="$profile.lang = 'es'">Añade un gadget a tu página personal en Google</xsl:when>
            <xsl:otherwise>Add a gadget to your personal page in Google</xsl:otherwise>
          </xsl:choose></xsl:attribute>
        </img>
      </a>
    </xsl:if>
  </xsl:template>

  <!-- Template taken from docbook-xsl to remove the type attribute in ols -->
  <xsl:template match="orderedlist">
    <xsl:variable name="start">
      <xsl:call-template name="orderedlist-starting-number"/>
    </xsl:variable>

    <xsl:variable name="numeration">
      <xsl:call-template name="list.numeration"/>
    </xsl:variable>

    <xsl:variable name="type">
      <xsl:choose>
        <xsl:when test="$numeration='arabic'">1</xsl:when>
        <xsl:when test="$numeration='loweralpha'">a</xsl:when>
        <xsl:when test="$numeration='lowerroman'">i</xsl:when>
        <xsl:when test="$numeration='upperalpha'">A</xsl:when>
        <xsl:when test="$numeration='upperroman'">I</xsl:when>
        <!-- What!? This should never happen -->
        <xsl:otherwise>
          <xsl:message>
            <xsl:text>Unexpected numeration: </xsl:text>
            <xsl:value-of select="$numeration"/>
          </xsl:message>
          <xsl:value-of select="1"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <div>
      <xsl:apply-templates select="." mode="class.attribute"/>
      <xsl:call-template name="anchor"/>

      <xsl:if test="title">
        <xsl:call-template name="formal.object.heading"/>
      </xsl:if>

      <!-- Preserve order of PIs and comments -->
      <xsl:apply-templates select="*[not(self::listitem                   or self::title                   or self::titleabbrev)]                 |comment()[not(preceding-sibling::listitem)]                 |processing-instruction()[not(preceding-sibling::listitem)]"/>

      <ol>
        <xsl:if test="$start != '1'">
          <xsl:attribute name="start">
            <xsl:value-of select="$start"/>
          </xsl:attribute>
        </xsl:if>
        <!--
        <xsl:if test="$numeration != ''">
          <xsl:attribute name="type">
            <xsl:value-of select="$type"/>
          </xsl:attribute>
        </xsl:if>
        -->
        <xsl:if test="@spacing='compact'">
          <xsl:attribute name="compact">
            <xsl:value-of select="@spacing"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:apply-templates select="listitem                     |comment()[preceding-sibling::listitem]                     |processing-instruction()[preceding-sibling::listitem]"/>
      </ol>
    </div>
  </xsl:template>
</xsl:stylesheet>