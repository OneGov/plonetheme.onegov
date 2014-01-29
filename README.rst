plonetheme.onegov
=================

This is the default theme for all OneGov Plone modules (http://onegov.ch).

.. image:: https://raw.github.com/OneGov/plonetheme.onegov/master/docs/screenshot_onegov.png


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


Links
-----

- Github project repository: https://github.com/OneGov/plonetheme.onegov
- Issue tracker: https://github.com/OneGov/plonetheme.onegov/issues
- Continuous integration: https://jenkins.4teamwork.ch/search?q=plonetheme.onegov


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``plonetheme.onegov`` is licensed under GNU General Public License, version 2.
