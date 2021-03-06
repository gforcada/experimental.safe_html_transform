from Products.CMFPlone import PloneMessageFactory as _
from plone.app.registry.browser import controlpanel
# from Products.CMFPlone.interfaces import IFilterSchema
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.registry.interfaces import IRegistry
from zope.interface import Interface
from zope.component import adapts
from zope import schema
from zope.component import getUtility
from zope.interface import implements


class IPloneSiteRoot(ISiteRoot, INavigationRoot):
    """
    Marker interface for the object which serves as the root of a
    Plone site.
    """


class ITagAttrPair(Interface):
    tags = schema.TextLine(title=u"tags")
    attributes = schema.TextLine(title=u"attributes")


class TagAttrPair:
    implements(ITagAttrPair)

    def __init__(self, tags='', attributes=''):
        self.tags = tags
        self.attributes = attributes


class IFilterTagsSchema(Interface):
    nasty_tags = schema.List(
        title=_(u'Nasty tags'),
        description=_(u"These tags, and their content are completely blocked "
                      "when a page is saved or rendered."),
        default=[u'applet', u'embed', u'object', u'script'],
        value_type=schema.TextLine(),
        required=False
    )

    stripped_tags = schema.List(
        title=_(u'Stripped tags'),
        description=_(u"These tags are stripped when saving or rendering, "
                      "but any content is preserved."),
        default=[u'font', ],
        value_type=schema.TextLine(),
        required=False
    )

    custom_tags = schema.List(
        title=_(u'Custom tags'),
        description=_(u"Add tag names here for tags which are not part of "
                      "XHTML but which should be permitted."),
        default=[],
        value_type=schema.TextLine(),
        required=False
    )


class IFilterAttributesSchema(Interface):
    stripped_attributes = schema.List(
        title=_(u'Stripped attributes'),
        description=_(u"These attributes are stripped from any tag when "
                      "saving."),
        default=(u'dir lang valign halign border frame rules cellspacing '
                 'cellpadding bgcolor').split(),
        value_type=schema.TextLine(),
        required=False)

#    stripped_combinations = schema.List(
#        title=_(u'Stripped combinations'),
#        description=_(u"These attributes are stripped from those tags when "
#                      "saving."),
#        default=[],
#        #default=u'dir lang valign halign border frame rules cellspacing
#        # cellpadding bgcolor'.split()
#        value_type=schema.Object(ITagAttrPair, title=u"combination"),
#        required=False)


class IFilterEditorSchema(Interface):

    style_whitelist = schema.List(
        title=_(u'Permitted styles'),
        description=_(u'These CSS styles are allowed in style attributes.'),
        default=u'text-align list-style-type float'.split(),
        value_type=schema.TextLine(),
        required=False)

    class_blacklist = schema.List(
        title=_(u'Filtered classes'),
        description=_(u'These class names are not allowed in class '
                      'attributes.'),
        default=[],
        value_type=schema.TextLine(),
        required=False)


class IFilterSchema(IFilterTagsSchema, IFilterAttributesSchema,
                    IFilterEditorSchema):
    """Combined schema for the adapter lookup.
    """


# filtertagset = FormFieldsets(IFilterTagsSchema)
# filtertagset.id = 'filtertags'
# filtertagset.label = _(u'label_filtertags', default=u'Tags')
#
# filterattributes = FormFieldsets(IFilterAttributesSchema)
# filterattributes.id = 'filterattributes'
# filterattributes.label = _(u'label_filterattributes', default=u'Attributes')
#
# filtereditor = FormFieldsets(IFilterEditorSchema)
# filtereditor.id = 'filtereditor'
# filtereditor.label = _(u'filterstyles', default=u'Styles')
#
# tagattr_widget = CustomWidgetFactory(ObjectWidget, TagAttrPair)
# combination_widget = CustomWidgetFactory(ListSequenceWidget,
#                                         subwidget=tagattr_widget)


class FilterControlPanelForm(controlpanel.RegistryEditForm):

    id = "FilterControlPanel"
    label = _("HTML Filter settings")
    description = _("Plone filters HTML tags that are considered security "
                    "risks. Be aware of the implications before making "
                    "changes below. By default only tags defined in XHTML "
                    "are permitted. In particular, to allow 'embed' as a tag "
                    "you must both remove it from 'Nasty tags' and add it to "
                    "'Custom tags'. Although the form will update "
                    "immediately to show any changes you make, your changes "
                    "are not saved until you press the 'Save' button.")
    form_name = _("HTML Filter settings")
    schema = IFilterSchema
    schema_prefix = "plone"

#    form_fields = FormFieldsets(filtertagset, filterattributes, filtereditor)
#    form_fields['stripped_combinations'].custom_widget = combination_widget

    # form_fields = FormFieldsets(searchset)
    # form_fields['types_not_searched'].custom_widget = MCBThreeColumnWidget
    # form_fields['types_not_searched'].custom_widget.cssClass='label'

    def updateFields(self):
        super(FilterControlPanelForm, self).updateFields()


class FilterControlPanel(controlpanel.ControlPanelFormWrapper):
    form = FilterControlPanelForm


class FilterControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(IFilterSchema)

    def __init__(self, context):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IFilterSchema, prefix="plone")

    def get_nasty_tags(self):
        return self.settings.nasty_tags

    def set_nasty_tags(self, value):
        self.settings.nasty_tags = value

    def get_stripped_tags(self):
        return self.settings.stripped_tags

    def set_stripped_tags(self, value):
        self.settings.stripped_tags = value

    def get_custom_tags(self):
        return self.settings.custom_tags

    def set_custom_tags(self, value):
        self.settings.custom_tags = value

    def get_stripped_attributes(self):
        return self.settings.stripped_attributes

    def set_stripped_attributes(self, value):
        self.settings.stripped_attributes = value

    def get_style_whitelist(self):
        return self.settings.style_whitelist

    def set_style_whitelist(self, value):
        self.settings.style_whitelist = value

    def get_class_blacklist(self):
        return self.settings.class_blacklist

    def set_class_blacklist(self, value):
        self.settings.class_blacklist = value

    nasty_tags = property(get_nasty_tags, set_nasty_tags)
    stripped_tags = property(get_stripped_tags, set_stripped_tags)
    custom_tags = property(get_custom_tags, set_custom_tags)
    stripped_attributes = property(
        get_stripped_attributes,
        set_stripped_attributes
    )
    style_whitelist = property(get_style_whitelist, set_style_whitelist)
    class_blacklist = property(get_class_blacklist, set_class_blacklist)
