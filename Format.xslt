<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- Extracts the SQL Server trace data to columnar format -->
<!-- Author: consultuning@gmail.com -->
<!-- Last updated: 4/6/2011 -->
<xsl:output method="xml"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/">
<Events>
<xsl:apply-templates select="TraceData/Events" />
</Events>
</xsl:template>

<xsl:template match="Event">
<Event>
<Name><xsl:value-of select="@name" /></Name>
<xsl:for-each select="Column">
<xsl:variable name="ColumnId" select="@name" />
<xsl:element name="{$ColumnId}">
<xsl:value-of select="." />
</xsl:element>
</xsl:for-each>
</Event>
</xsl:template>

</xsl:stylesheet>