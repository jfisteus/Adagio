<?xml version="1.0" encoding="UTF-8"?>

<!--
  Copyright (C) 2008 Carlos III University of Madrid
  This file is part of Adagio: Agile Distributed Authoring Integrated Toolkit

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
  xmlns:xi="http://www.w3.org/2001/XInclude"
  version="1.0" exclude-result-prefixes="exsl xi">

  <!-- Obtain genearl adagio variables -->
  <xsl:import href="GeneralParams.xsl"/>

  <xsl:param name="adagio.rss.time.to.live">30</xsl:param>
  <xsl:param name="adagio.rss.title">Rss title goes here</xsl:param>
  <xsl:param name="adagio.rss.description">Descripción del canal</xsl:param>

  <!-- Parameter to put in links to the main site documentation -->
  <xsl:param name="adagio.rss.main.site.url">http://bogus.net</xsl:param>

  <!-- Name of the file containing the feed (no prefix) -->
  <xsl:param name="adagio.rss.filename"/>

  <!-- URL pointing to the XML file containing the feed -->
  <xsl:param name="adagio.rss.channel.url"><xsl:value-of
  select="$adagio.rss.filename"/></xsl:param>

  <!-- Prefix of the type http://......./a/b/c to use for material links -->
  <xsl:param name="adagio.rss.item.url.prefix">Your prefix goes here</xsl:param>

  <xsl:param name="adagio.rss.language">en</xsl:param>
  <xsl:param name="adagio.rss.copyright">Copyright goes here</xsl:param>
  <xsl:param name="adagio.rss.author.email">author@bogus.net (Author name)</xsl:param>
  <xsl:param name="adagio.rss.author.name">Author name goes here</xsl:param>
  <xsl:param name="adagio.rss.subtitle">Rss subtitle goes here</xsl:param>
  <xsl:param name="adagio.rss.summary">Rss summary goes here</xsl:param>
  <xsl:param name="adagio.rss.explicit">No</xsl:param>
  <xsl:param name="adagio.rss.image.url">http://image.net/bogusimage.png</xsl:param>
  <xsl:param name="adagio.rss.image.desc"></xsl:param>
  <xsl:param name="adagio.rss.image.width">88</xsl:param>
  <xsl:param name="adagio.rss.image.height">88</xsl:param>
  <xsl:param name="adagio.rss.category">Education</xsl:param>
  <xsl:param name="adagio.rss.subcategory">Higher Education</xsl:param>
  <xsl:param name="adagio.rss.max.items">10</xsl:param>
  <xsl:param name="adagio.rss.check.pubdate">0</xsl:param>
  <xsl:param name="adagio.rss.force.date"></xsl:param>
  <xsl:param name="adagio.rss.date.rfc822"></xsl:param>
  <xsl:param name="adagio.rss.self.atom.link"><xsl:value-of
  select="$adagio.rss.channel.url"/></xsl:param>
  <xsl:param name="adagio.rss.numitems.max">1000000</xsl:param>
  <xsl:param name="adagio.rss.autolink">false</xsl:param>
  <xsl:param name="adagio.rss.autoguid">false</xsl:param>

  <xsl:param name="adagio.rss.debug"/>
</xsl:stylesheet>
