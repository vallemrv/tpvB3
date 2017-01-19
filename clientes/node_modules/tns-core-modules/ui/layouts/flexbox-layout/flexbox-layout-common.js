var layout_base_1 = require("ui/layouts/layout-base");
var view_1 = require("ui/core/view");
var proxy_1 = require("ui/core/proxy");
var dependency_observable_1 = require("ui/core/dependency-observable");
var special_properties_1 = require("ui/builder/special-properties");
var platform_1 = require("platform");
var ORDER_DEFAULT = 1;
var FLEX_GROW_DEFAULT = 0.0;
var FLEX_SHRINK_DEFAULT = 1.0;
var affectsLayout = platform_1.isAndroid ? dependency_observable_1.PropertyMetadataSettings.None : dependency_observable_1.PropertyMetadataSettings.AffectsLayout;
var FlexDirection;
(function (FlexDirection) {
    FlexDirection.ROW = "row";
    FlexDirection.ROW_REVERSE = "row-reverse";
    FlexDirection.COLUMN = "column";
    FlexDirection.COLUMN_REVERSE = "column-reverse";
})(FlexDirection = exports.FlexDirection || (exports.FlexDirection = {}));
var validFlexDirection = {
    "row": true,
    "row-reverse": true,
    "column": true,
    "column-reverse": true
};
function validateFlexDirection(value) {
    return value in validFlexDirection;
}
var FlexWrap;
(function (FlexWrap) {
    FlexWrap.NOWRAP = "nowrap";
    FlexWrap.WRAP = "wrap";
    FlexWrap.WRAP_REVERSE = "wrap-reverse";
})(FlexWrap = exports.FlexWrap || (exports.FlexWrap = {}));
var validFlexWrap = {
    "nowrap": true,
    "wrap": true,
    "wrap-reverse": true
};
function validateFlexWrap(value) {
    return value in validFlexWrap;
}
var JustifyContent;
(function (JustifyContent) {
    JustifyContent.FLEX_START = "flex-start";
    JustifyContent.FLEX_END = "flex-end";
    JustifyContent.CENTER = "center";
    JustifyContent.SPACE_BETWEEN = "space-between";
    JustifyContent.SPACE_AROUND = "space-around";
})(JustifyContent = exports.JustifyContent || (exports.JustifyContent = {}));
var validJustifyContent = {
    "flex-start": true,
    "flex-end": true,
    "center": true,
    "space-between": true,
    "space-around": true
};
var FlexBasisPercent;
(function (FlexBasisPercent) {
    FlexBasisPercent.DEFAULT = -1;
})(FlexBasisPercent = exports.FlexBasisPercent || (exports.FlexBasisPercent = {}));
function validateJustifyContent(value) {
    return value in validJustifyContent;
}
var AlignItems;
(function (AlignItems) {
    AlignItems.FLEX_START = "flex-start";
    AlignItems.FLEX_END = "flex-end";
    AlignItems.CENTER = "center";
    AlignItems.BASELINE = "baseline";
    AlignItems.STRETCH = "stretch";
})(AlignItems = exports.AlignItems || (exports.AlignItems = {}));
var validAlignItems = {
    "flex-start": true,
    "flex-end": true,
    "center": true,
    "baseline": true,
    "stretch": true
};
function validateAlignItems(value) {
    return value in validAlignItems;
}
var AlignContent;
(function (AlignContent) {
    AlignContent.FLEX_START = "flex-start";
    AlignContent.FLEX_END = "flex-end";
    AlignContent.CENTER = "center";
    AlignContent.SPACE_BETWEEN = "space-between";
    AlignContent.SPACE_AROUND = "space-around";
    AlignContent.STRETCH = "stretch";
})(AlignContent = exports.AlignContent || (exports.AlignContent = {}));
var validAlignContent = {
    "flex-start": true,
    "flex-end": true,
    "center": true,
    "space-between": true,
    "space-around": true,
    "stretch": true
};
function validateAlignContent(value) {
    return value in validAlignContent;
}
var AlignSelf;
(function (AlignSelf) {
    AlignSelf.AUTO = "auto";
    AlignSelf.FLEX_START = "flex-start";
    AlignSelf.FLEX_END = "flex-end";
    AlignSelf.CENTER = "center";
    AlignSelf.BASELINE = "baseline";
    AlignSelf.STRETCH = "stretch";
})(AlignSelf = exports.AlignSelf || (exports.AlignSelf = {}));
function validateArgs(element) {
    if (!element) {
        throw new Error("element cannot be null or undefinied.");
    }
    return element;
}
var FlexboxLayoutBase = (function (_super) {
    __extends(FlexboxLayoutBase, _super);
    function FlexboxLayoutBase() {
        _super.call(this);
    }
    Object.defineProperty(FlexboxLayoutBase.prototype, "flexDirection", {
        get: function () {
            return this._getValue(FlexboxLayoutBase.flexDirectionProperty);
        },
        set: function (value) {
            this._setValue(FlexboxLayoutBase.flexDirectionProperty, value);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FlexboxLayoutBase.prototype, "flexWrap", {
        get: function () {
            return this._getValue(FlexboxLayoutBase.flexWrapProperty);
        },
        set: function (value) {
            this._setValue(FlexboxLayoutBase.flexWrapProperty, value);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FlexboxLayoutBase.prototype, "justifyContent", {
        get: function () {
            return this._getValue(FlexboxLayoutBase.justifyContentProperty);
        },
        set: function (value) {
            this._setValue(FlexboxLayoutBase.justifyContentProperty, value);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FlexboxLayoutBase.prototype, "alignItems", {
        get: function () {
            return this._getValue(FlexboxLayoutBase.alignItemsProperty);
        },
        set: function (value) {
            this._setValue(FlexboxLayoutBase.alignItemsProperty, value);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FlexboxLayoutBase.prototype, "alignContent", {
        get: function () {
            return this._getValue(FlexboxLayoutBase.alignContentProperty);
        },
        set: function (value) {
            this._setValue(FlexboxLayoutBase.alignContentProperty, value);
        },
        enumerable: true,
        configurable: true
    });
    FlexboxLayoutBase.setOrder = function (view, order) {
        validateArgs(view)._setValue(FlexboxLayoutBase.orderProperty, order);
    };
    FlexboxLayoutBase.getOrder = function (view) {
        return validateArgs(view)._getValue(FlexboxLayoutBase.orderProperty);
    };
    FlexboxLayoutBase.setFlexGrow = function (view, grow) {
        validateArgs(view)._setValue(FlexboxLayoutBase.flexGrowProperty, grow);
    };
    FlexboxLayoutBase.getFlexGrow = function (view) {
        return validateArgs(view)._getValue(FlexboxLayoutBase.flexGrowProperty);
    };
    FlexboxLayoutBase.setFlexShrink = function (view, shrink) {
        validateArgs(view)._setValue(FlexboxLayoutBase.flexShrinkProperty, shrink);
    };
    FlexboxLayoutBase.getFlexShrink = function (view) {
        return validateArgs(view)._getValue(FlexboxLayoutBase.flexShrinkProperty);
    };
    FlexboxLayoutBase.setAlignSelf = function (view, align) {
        validateArgs(view)._setValue(FlexboxLayoutBase.alignSelfProperty, align);
    };
    FlexboxLayoutBase.getAlignSelf = function (view) {
        return validateArgs(view)._getValue(FlexboxLayoutBase.alignSelfProperty);
    };
    FlexboxLayoutBase.setFlexWrapBefore = function (view, wrap) {
        view._setValue(FlexboxLayoutBase.flexWrapBeforeProperty, wrap);
    };
    FlexboxLayoutBase.getFlexWrapBefore = function (view) {
        return view._getValue(FlexboxLayoutBase.flexWrapBeforeProperty);
    };
    FlexboxLayoutBase.childHandler = function (args) {
        var element = args.object;
        if (!(element instanceof view_1.View)) {
            throw new Error("Element is not View or its descendant.");
        }
        var flexbox = element.parent;
        if (flexbox instanceof FlexboxLayoutBase) {
            flexbox.invalidate();
        }
    };
    FlexboxLayoutBase.flexDirectionProperty = new dependency_observable_1.Property("flexDirection", "FlexboxLayout", new proxy_1.PropertyMetadata("row", affectsLayout, undefined, validateFlexDirection, function (args) { return args.object.setNativeFlexDirection(args.newValue); }));
    FlexboxLayoutBase.flexWrapProperty = new dependency_observable_1.Property("flexWrap", "FlexboxLayout", new proxy_1.PropertyMetadata("nowrap", affectsLayout, undefined, validateFlexWrap, function (args) { return args.object.setNativeFlexWrap(args.newValue); }));
    FlexboxLayoutBase.justifyContentProperty = new dependency_observable_1.Property("justifyContent", "FlexboxLayout", new proxy_1.PropertyMetadata("flex-start", affectsLayout, undefined, validateJustifyContent, function (args) { return args.object.setNativeJustifyContent(args.newValue); }));
    FlexboxLayoutBase.alignItemsProperty = new dependency_observable_1.Property("alignItems", "FlexboxLayout", new proxy_1.PropertyMetadata("stretch", affectsLayout, undefined, validateAlignItems, function (args) { return args.object.setNativeAlignItems(args.newValue); }));
    FlexboxLayoutBase.alignContentProperty = new dependency_observable_1.Property("alignContent", "FlexboxLayout", new proxy_1.PropertyMetadata("stretch", affectsLayout, undefined, validateAlignContent, function (args) { return args.object.setNativeAlignContent(args.newValue); }));
    FlexboxLayoutBase.orderProperty = new dependency_observable_1.Property("order", "FlexboxLayout", new proxy_1.PropertyMetadata(ORDER_DEFAULT, dependency_observable_1.PropertyMetadataSettings.None, FlexboxLayoutBase.childHandler));
    FlexboxLayoutBase.flexGrowProperty = new dependency_observable_1.Property("flexGrow", "FlexboxLayout", new proxy_1.PropertyMetadata(FLEX_GROW_DEFAULT, dependency_observable_1.PropertyMetadataSettings.None, FlexboxLayoutBase.childHandler));
    FlexboxLayoutBase.flexShrinkProperty = new dependency_observable_1.Property("flexShrink", "FlexboxLayout", new proxy_1.PropertyMetadata(FLEX_SHRINK_DEFAULT, dependency_observable_1.PropertyMetadataSettings.None, FlexboxLayoutBase.childHandler));
    FlexboxLayoutBase.flexWrapBeforeProperty = new dependency_observable_1.Property("flexWrapBefore", "FlexboxLayout", new proxy_1.PropertyMetadata(false, dependency_observable_1.PropertyMetadataSettings.None, FlexboxLayoutBase.childHandler));
    FlexboxLayoutBase.alignSelfProperty = new dependency_observable_1.Property("alignSelf", "FlexboxLayout", new proxy_1.PropertyMetadata(AlignSelf.AUTO, dependency_observable_1.PropertyMetadataSettings.None, FlexboxLayoutBase.childHandler));
    return FlexboxLayoutBase;
}(layout_base_1.LayoutBase));
exports.FlexboxLayoutBase = FlexboxLayoutBase;
special_properties_1.registerSpecialProperty("order", function (instance, propertyValue) {
    FlexboxLayoutBase.setOrder(instance, !isNaN(+propertyValue) && +propertyValue);
});
special_properties_1.registerSpecialProperty("flexGrow", function (instance, propertyValue) {
    FlexboxLayoutBase.setFlexGrow(instance, !isNaN(+propertyValue) && +propertyValue);
});
special_properties_1.registerSpecialProperty("flexShrink", function (instance, propertyValue) {
    FlexboxLayoutBase.setFlexShrink(instance, !isNaN(+propertyValue) && +propertyValue);
});
special_properties_1.registerSpecialProperty("alignSelf", function (instance, propertyValue) {
    FlexboxLayoutBase.setAlignSelf(instance, propertyValue);
});
special_properties_1.registerSpecialProperty("flexWrapBefore", function (instance, propertyValue) {
    FlexboxLayoutBase.setFlexWrapBefore(instance, propertyValue);
});
//# sourceMappingURL=flexbox-layout-common.js.map