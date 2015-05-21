plonetheme.onegov
=================

This is the default theme for all OneGov Plone modules (http://onegov.ch).

.. image:: https://raw.github.com/OneGov/plonetheme.onegov/master/docs/screenshot_onegov.png

**Important** this package doesn't work with python 2.6, it requires at least python 2.7

Usage
-----

- Add ``plonetheme.onegov`` to your buildout configuration:

::

    [instance]
    eggs +=
        plonetheme.onegov

- Install the generic import profile.

Features
--------
- Customize styles in control panel.
- Responsive design for tablets and smartphones
- Special path bar with children


Layout customizations
---------------------

Theme is SCSS based and styles most things with variables which can easily be customized
in a control panel.

Just visit the customization view: http://localhost:8080/Plone/customstyles_form

Here are some examples how the Layout can be customized:

.. image:: https://raw.github.com/OneGov/plonetheme.onegov/master/docs/screenshot_zg_ch.png

.. image:: https://raw.github.com/OneGov/plonetheme.onegov/master/docs/screenshot_menzingen.png

.. image:: https://raw.github.com/OneGov/plonetheme.onegov/master/docs/screenshot_custom.png


Additional SCSS
---------------

You can easily register custom SCSS files in your addon package using ZCML, if you need to customize
more than available through the web:

.. code:: xml

    <configure
        xmlns:theme="http://namespaces.zope.org/plonetheme.onegov">

        <include package="plonetheme.onegov" />
        <theme:add_scss path="resources/custom.scss" />

    </configure>

The SCSS files can also be restricted to a specific context interface or a specific request layer.
Be aware that the context interface applies to the context the styles are rendered on, which is either
the Plone site root or an `INavigationRoot` object.

.. code:: xml

    <configure
        xmlns:theme="http://namespaces.zope.org/plonetheme.onegov">

        <include package="plonetheme.onegov" />
        <theme:add_scss
            path="resources/custom.scss"
            for="my.package.interfaces.ISubsite"
            layer="my.package.interfaces.IMyPackageLayer" />

    </configure>

Flyout navigation
-----------------
This theme comes with a flyout navigation. If you click on an element in the global navigation you get the children as a flyout navigation and also a link to go 'direct to' the element you clicked on.
This behavior can be disabled in the plone.app.registry, using the setting ``plonetheme.onegov.flyout_navigation``.

.. image:: https://raw.github.com/OneGov/plonetheme.onegov/master/docs/screenshot_flyout_navigation.png


Special path bar
----------------
For another fast way to navigate between content, this theme includes a special path bar, which shows the breadcrumb's children.
This behavior can be disabled in the plone.app.registry, using the setting ``plonetheme.onegov.flyout_breadcrumbs``.

.. image:: https://raw.github.com/OneGov/plonetheme.onegov/master/docs/screenshot_flyout_breadcrumbs.png

Special filter form
-------------------

This Theme provides an alternativ search/filter mockup.
The Implementation needs to be done by yourself. `For an example check the Solr search form of zg.ch <http://www.zg.ch/@@search>`_.

.. image:: https://raw.github.com/OneGov/plonetheme.onegov/master/docs/screenshot_filter.png



Print
-----
Known issue page-break in WebKit
https://bugs.webkit.org/show_bug.cgi?id=5097

Links
-----

- Github project repository: https://github.com/OneGov/plonetheme.onegov
- Issue tracker: https://github.com/OneGov/plonetheme.onegov/issues
- Continuous integration: https://jenkins.4teamwork.ch/search?q=plonetheme.onegov


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``plonetheme.onegov`` is licensed under GNU General Public License, version 2.
