// Transcrypt'ed from Python, 2019-01-14 14:01:45
var __name__ = 'org.transcrypt.__runtime__';

function __nest__ (headObject, tailNames, value) {
    var current = headObject;
    if (tailNames != '') {
        var tailChain = tailNames.split ('.');
        var firstNewIndex = tailChain.length;
        for (var index = 0; index < tailChain.length; index++) {
            if (!current.hasOwnProperty (tailChain [index])) {
                firstNewIndex = index;
                break;
            }
            current = current [tailChain [index]];
        }
        for (var index = firstNewIndex; index < tailChain.length; index++) {
            current [tailChain [index]] = {};
            current = current [tailChain [index]];
        }
    }
    for (let attrib of Object.getOwnPropertyNames (value)) {
        Object.defineProperty (current, attrib, {
            get () {return value [attrib];},
            enumerable: true,
            configurable: true
        });
    }
}function __get__ (self, func, quotedFuncName) {
    if (self) {
        if (self.hasOwnProperty ('__class__') || typeof self == 'string' || self instanceof String) {
            if (quotedFuncName) {
                Object.defineProperty (self, quotedFuncName, {
                    value: function () {
                        var args = [] .slice.apply (arguments);
                        return func.apply (null, [self] .concat (args));
                    },
                    writable: true,
                    enumerable: true,
                    configurable: true
                });
            }
            return function () {
                var args = [] .slice.apply (arguments);
                return func.apply (null, [self] .concat (args));
            };
        }
        else {
            return func;
        }
    }
    else {
        return func;
    }
}var py_metatype = {
    __name__: 'type',
    __bases__: [],
    __new__: function (meta, name, bases, attribs) {
        var cls = function () {
            var args = [] .slice.apply (arguments);
            return cls.__new__ (args);
        };
        for (var index = bases.length - 1; index >= 0; index--) {
            var base = bases [index];
            for (var attrib in base) {
                var descrip = Object.getOwnPropertyDescriptor (base, attrib);
                Object.defineProperty (cls, attrib, descrip);
            }
            for (let symbol of Object.getOwnPropertySymbols (base)) {
                let descrip = Object.getOwnPropertyDescriptor (base, symbol);
                Object.defineProperty (cls, symbol, descrip);
            }
        }
        cls.__metaclass__ = meta;
        cls.__name__ = name.startsWith ('py_') ? name.slice (3) : name;
        cls.__bases__ = bases;
        for (var attrib in attribs) {
            var descrip = Object.getOwnPropertyDescriptor (attribs, attrib);
            Object.defineProperty (cls, attrib, descrip);
        }
        for (let symbol of Object.getOwnPropertySymbols (attribs)) {
            let descrip = Object.getOwnPropertyDescriptor (attribs, symbol);
            Object.defineProperty (cls, symbol, descrip);
        }
        return cls;
    }
};
py_metatype.__metaclass__ = py_metatype;
var object = {
    __init__: function (self) {},
    __metaclass__: py_metatype,
    __name__: 'object',
    __bases__: [],
    __new__: function (args) {
        var instance = Object.create (this, {__class__: {value: this, enumerable: true}});
        if ('__getattr__' in this || '__setattr__' in this) {
            instance = new Proxy (instance, {
                get: function (target, name) {
                    let result = target [name];
                    if (result == undefined) {
                        return target.__getattr__ (name);
                    }
                    else {
                        return result;
                    }
                },
                set: function (target, name, value) {
                    try {
                        target.__setattr__ (name, value);
                    }
                    catch (exception) {
                        target [name] = value;
                    }
                    return true;
                }
            });
        }
        this.__init__.apply (null, [instance] .concat (args));
        return instance;
    }
};
function __class__ (name, bases, attribs, meta) {
    if (meta === undefined) {
        meta = bases [0] .__metaclass__;
    }
    return meta.__new__ (meta, name, bases, attribs);
}function __call__ (/* <callee>, <this>, <params>* */) {
    var args = [] .slice.apply (arguments);
    if (typeof args [0] == 'object' && '__call__' in args [0]) {
        return args [0] .__call__ .apply (args [1], args.slice (2));
    }
    else {
        return args [0] .apply (args [1], args.slice (2));
    }
}function __kwargtrans__ (anObject) {
    anObject.__kwargtrans__ = null;
    anObject.constructor = Object;
    return anObject;
}
function __setproperty__ (anObject, name, descriptor) {
    if (!anObject.hasOwnProperty (name)) {
        Object.defineProperty (anObject, name, descriptor);
    }
}
function __in__ (element, container) {
    if (container === undefined || container === null) {
        return false;
    }
    if (container.__contains__ instanceof Function) {
        return container.__contains__ (element);
    }
    else {
        return (
            container.indexOf ?
            container.indexOf (element) > -1 :
            container.hasOwnProperty (element)
        );
    }
}function __specialattrib__ (attrib) {
    return (attrib.startswith ('__') && attrib.endswith ('__')) || attrib == 'constructor' || attrib.startswith ('py_');
}function len (anObject) {
    if (anObject === undefined || anObject === null) {
        return 0;
    }
    if (anObject.__len__ instanceof Function) {
        return anObject.__len__ ();
    }
    if (anObject.length !== undefined) {
        return anObject.length;
    }
    var length = 0;
    for (var attr in anObject) {
        if (!__specialattrib__ (attr)) {
            length++;
        }
    }
    return length;
}function __t__ (target) {
    return (
        target === undefined || target === null ? false :
        ['boolean', 'number'] .indexOf (typeof target) >= 0 ? target :
        target.__bool__ instanceof Function ? (target.__bool__ () ? target : false) :
        target.__len__ instanceof Function ?  (target.__len__ () !== 0 ? target : false) :
        target instanceof Function ? target :
        len (target) !== 0 ? target :
        false
    );
}
function float (any) {
    if (any == 'inf') {
        return Infinity;
    }
    else if (any == '-inf') {
        return -Infinity;
    }
    else if (any == 'nan') {
        return NaN;
    }
    else if (isNaN (parseFloat (any))) {
        if (any === false) {
            return 0;
        }
        else if (any === true) {
            return 1;
        }
        else {
            throw ValueError ("could not convert string to float: '" + str(any) + "'", new Error ());
        }
    }
    else {
        return +any;
    }
}float.__name__ = 'float';
float.__bases__ = [object];
function int (any) {
    return float (any) | 0
}int.__name__ = 'int';
int.__bases__ = [object];
function bool (any) {
    return !!__t__ (any);
}bool.__name__ = 'bool';
bool.__bases__ = [int];
function py_typeof (anObject) {
    var aType = typeof anObject;
    if (aType == 'object') {
        try {
            return '__class__' in anObject ? anObject.__class__ : object;
        }
        catch (exception) {
            return aType;
        }
    }
    else {
        return (
            aType == 'boolean' ? bool :
            aType == 'string' ? str :
            aType == 'number' ? (anObject % 1 == 0 ? int : float) :
            null
        );
    }
}function issubclass (aClass, classinfo) {
    if (classinfo instanceof Array) {
        for (let aClass2 of classinfo) {
            if (issubclass (aClass, aClass2)) {
                return true;
            }
        }
        return false;
    }
    try {
        var aClass2 = aClass;
        if (aClass2 == classinfo) {
            return true;
        }
        else {
            var bases = [].slice.call (aClass2.__bases__);
            while (bases.length) {
                aClass2 = bases.shift ();
                if (aClass2 == classinfo) {
                    return true;
                }
                if (aClass2.__bases__.length) {
                    bases = [].slice.call (aClass2.__bases__).concat (bases);
                }
            }
            return false;
        }
    }
    catch (exception) {
        return aClass == classinfo || classinfo == object;
    }
}function isinstance (anObject, classinfo) {
    try {
        return '__class__' in anObject ? issubclass (anObject.__class__, classinfo) : issubclass (py_typeof (anObject), classinfo);
    }
    catch (exception) {
        return issubclass (py_typeof (anObject), classinfo);
    }
}function repr (anObject) {
    try {
        return anObject.__repr__ ();
    }
    catch (exception) {
        try {
            return anObject.__str__ ();
        }
        catch (exception) {
            try {
                if (anObject == null) {
                    return 'None';
                }
                else if (anObject.constructor == Object) {
                    var result = '{';
                    var comma = false;
                    for (var attrib in anObject) {
                        if (!__specialattrib__ (attrib)) {
                            if (attrib.isnumeric ()) {
                                var attribRepr = attrib;
                            }
                            else {
                                var attribRepr = '\'' + attrib + '\'';
                            }
                            if (comma) {
                                result += ', ';
                            }
                            else {
                                comma = true;
                            }
                            result += attribRepr + ': ' + repr (anObject [attrib]);
                        }
                    }
                    result += '}';
                    return result;
                }
                else {
                    return typeof anObject == 'boolean' ? anObject.toString () .capitalize () : anObject.toString ();
                }
            }
            catch (exception) {
                return '<object of type: ' + typeof anObject + '>';
            }
        }
    }
}var abs = Math.abs;
function __PyIterator__ (iterable) {
    this.iterable = iterable;
    this.index = 0;
}
__PyIterator__.prototype.__next__ = function() {
    if (this.index < this.iterable.length) {
        return this.iterable [this.index++];
    }
    else {
        throw StopIteration (new Error ());
    }
};
function __JsIterator__ (iterable) {
    this.iterable = iterable;
    this.index = 0;
}
__JsIterator__.prototype.next = function () {
    if (this.index < this.iterable.py_keys.length) {
        return {value: this.index++, done: false};
    }
    else {
        return {value: undefined, done: true};
    }
};
function list (iterable) {
    let instance = iterable ? Array.from (iterable) : [];
    return instance;
}
Array.prototype.__class__ = list;
list.__name__ = 'list';
list.__bases__ = [object];
Array.prototype.__iter__ = function () {return new __PyIterator__ (this);};
Array.prototype.__getslice__ = function (start, stop, step) {
    if (start < 0) {
        start = this.length + start;
    }
    if (stop == null) {
        stop = this.length;
    }
    else if (stop < 0) {
        stop = this.length + stop;
    }
    else if (stop > this.length) {
        stop = this.length;
    }
    if (step == 1) {
        return Array.prototype.slice.call(this, start, stop);
    }
    let result = list ([]);
    for (let index = start; index < stop; index += step) {
        result.push (this [index]);
    }
    return result;
};
Array.prototype.__setslice__ = function (start, stop, step, source) {
    if (start < 0) {
        start = this.length + start;
    }
    if (stop == null) {
        stop = this.length;
    }
    else if (stop < 0) {
        stop = this.length + stop;
    }
    if (step == null) {
        Array.prototype.splice.apply (this, [start, stop - start] .concat (source));
    }
    else {
        let sourceIndex = 0;
        for (let targetIndex = start; targetIndex < stop; targetIndex += step) {
            this [targetIndex] = source [sourceIndex++];
        }
    }
};
Array.prototype.__repr__ = function () {
    if (this.__class__ == set && !this.length) {
        return 'set()';
    }
    let result = !this.__class__ || this.__class__ == list ? '[' : this.__class__ == tuple ? '(' : '{';
    for (let index = 0; index < this.length; index++) {
        if (index) {
            result += ', ';
        }
        result += repr (this [index]);
    }
    if (this.__class__ == tuple && this.length == 1) {
        result += ',';
    }
    result += !this.__class__ || this.__class__ == list ? ']' : this.__class__ == tuple ? ')' : '}';    return result;
};
Array.prototype.__str__ = Array.prototype.__repr__;
Array.prototype.append = function (element) {
    this.push (element);
};
Array.prototype.py_clear = function () {
    this.length = 0;
};
Array.prototype.extend = function (aList) {
    this.push.apply (this, aList);
};
Array.prototype.insert = function (index, element) {
    this.splice (index, 0, element);
};
Array.prototype.remove = function (element) {
    let index = this.indexOf (element);
    if (index == -1) {
        throw ValueError ("list.remove(x): x not in list", new Error ());
    }
    this.splice (index, 1);
};
Array.prototype.index = function (element) {
    return this.indexOf (element);
};
Array.prototype.py_pop = function (index) {
    if (index == undefined) {
        return this.pop ();
    }
    else {
        return this.splice (index, 1) [0];
    }
};
Array.prototype.py_sort = function () {
    __sort__.apply  (null, [this].concat ([] .slice.apply (arguments)));
};
Array.prototype.__add__ = function (aList) {
    return list (this.concat (aList));
};
Array.prototype.__mul__ = function (scalar) {
    let result = this;
    for (let i = 1; i < scalar; i++) {
        result = result.concat (this);
    }
    return result;
};
Array.prototype.__rmul__ = Array.prototype.__mul__;
function tuple (iterable) {
    let instance = iterable ? [] .slice.apply (iterable) : [];
    instance.__class__ = tuple;
    return instance;
}
tuple.__name__ = 'tuple';
tuple.__bases__ = [object];
function set (iterable) {
    let instance = [];
    if (iterable) {
        for (let index = 0; index < iterable.length; index++) {
            instance.add (iterable [index]);
        }
    }
    instance.__class__ = set;
    return instance;
}
set.__name__ = 'set';
set.__bases__ = [object];
Array.prototype.__bindexOf__ = function (element) {
    element += '';
    let mindex = 0;
    let maxdex = this.length - 1;
    while (mindex <= maxdex) {
        let index = (mindex + maxdex) / 2 | 0;
        let middle = this [index] + '';
        if (middle < element) {
            mindex = index + 1;
        }
        else if (middle > element) {
            maxdex = index - 1;
        }
        else {
            return index;
        }
    }
    return -1;
};
Array.prototype.add = function (element) {
    if (this.indexOf (element) == -1) {
        this.push (element);
    }
};
Array.prototype.discard = function (element) {
    var index = this.indexOf (element);
    if (index != -1) {
        this.splice (index, 1);
    }
};
Array.prototype.isdisjoint = function (other) {
    this.sort ();
    for (let i = 0; i < other.length; i++) {
        if (this.__bindexOf__ (other [i]) != -1) {
            return false;
        }
    }
    return true;
};
Array.prototype.issuperset = function (other) {
    this.sort ();
    for (let i = 0; i < other.length; i++) {
        if (this.__bindexOf__ (other [i]) == -1) {
            return false;
        }
    }
    return true;
};
Array.prototype.issubset = function (other) {
    return set (other.slice ()) .issuperset (this);
};
Array.prototype.union = function (other) {
    let result = set (this.slice () .sort ());
    for (let i = 0; i < other.length; i++) {
        if (result.__bindexOf__ (other [i]) == -1) {
            result.push (other [i]);
        }
    }
    return result;
};
Array.prototype.intersection = function (other) {
    this.sort ();
    let result = set ();
    for (let i = 0; i < other.length; i++) {
        if (this.__bindexOf__ (other [i]) != -1) {
            result.push (other [i]);
        }
    }
    return result;
};
Array.prototype.difference = function (other) {
    let sother = set (other.slice () .sort ());
    let result = set ();
    for (let i = 0; i < this.length; i++) {
        if (sother.__bindexOf__ (this [i]) == -1) {
            result.push (this [i]);
        }
    }
    return result;
};
Array.prototype.symmetric_difference = function (other) {
    return this.union (other) .difference (this.intersection (other));
};
Array.prototype.py_update = function () {
    let updated = [] .concat.apply (this.slice (), arguments) .sort ();
    this.py_clear ();
    for (let i = 0; i < updated.length; i++) {
        if (updated [i] != updated [i - 1]) {
            this.push (updated [i]);
        }
    }
};
Array.prototype.__eq__ = function (other) {
    if (this.length != other.length) {
        return false;
    }
    if (this.__class__ == set) {
        this.sort ();
        other.sort ();
    }
    for (let i = 0; i < this.length; i++) {
        if (this [i] != other [i]) {
            return false;
        }
    }
    return true;
};
Array.prototype.__ne__ = function (other) {
    return !this.__eq__ (other);
};
Array.prototype.__le__ = function (other) {
    if (this.__class__ == set) {
        return this.issubset (other);
    }
    else {
        for (let i = 0; i < this.length; i++) {
            if (this [i] > other [i]) {
                return false;
            }
            else if (this [i] < other [i]) {
                return true;
            }
        }
        return true;
    }
};
Array.prototype.__ge__ = function (other) {
    if (this.__class__ == set) {
        return this.issuperset (other);
    }
    else {
        for (let i = 0; i < this.length; i++) {
            if (this [i] < other [i]) {
                return false;
            }
            else if (this [i] > other [i]) {
                return true;
            }
        }
        return true;
    }
};
Array.prototype.__lt__ = function (other) {
    return (
        this.__class__ == set ?
        this.issubset (other) && !this.issuperset (other) :
        !this.__ge__ (other)
    );
};
Array.prototype.__gt__ = function (other) {
    return (
        this.__class__ == set ?
        this.issuperset (other) && !this.issubset (other) :
        !this.__le__ (other)
    );
};
Uint8Array.prototype.__add__ = function (aBytes) {
    let result = new Uint8Array (this.length + aBytes.length);
    result.set (this);
    result.set (aBytes, this.length);
    return result;
};
Uint8Array.prototype.__mul__ = function (scalar) {
    let result = new Uint8Array (scalar * this.length);
    for (let i = 0; i < scalar; i++) {
        result.set (this, i * this.length);
    }
    return result;
};
Uint8Array.prototype.__rmul__ = Uint8Array.prototype.__mul__;
function str (stringable) {
    if (typeof stringable === 'number')
        return stringable.toString();
    else {
        try {
            return stringable.__str__ ();
        }
        catch (exception) {
            try {
                return repr (stringable);
            }
            catch (exception) {
                return String (stringable);
            }
        }
    }
}String.prototype.__class__ = str;
str.__name__ = 'str';
str.__bases__ = [object];
String.prototype.__iter__ = function () {};
String.prototype.__repr__ = function () {
    return (this.indexOf ('\'') == -1 ? '\'' + this + '\'' : '"' + this + '"') .py_replace ('\t', '\\t') .py_replace ('\n', '\\n');
};
String.prototype.__str__ = function () {
    return this;
};
String.prototype.capitalize = function () {
    return this.charAt (0).toUpperCase () + this.slice (1);
};
String.prototype.endswith = function (suffix) {
    if (suffix instanceof Array) {
        for (var i=0;i<suffix.length;i++) {
            if (this.slice (-suffix[i].length) == suffix[i])
                return true;
        }
    } else
        return suffix == '' || this.slice (-suffix.length) == suffix;
    return false;
};
String.prototype.find = function (sub, start) {
    return this.indexOf (sub, start);
};
String.prototype.__getslice__ = function (start, stop, step) {
    if (start < 0) {
        start = this.length + start;
    }
    if (stop == null) {
        stop = this.length;
    }
    else if (stop < 0) {
        stop = this.length + stop;
    }
    var result = '';
    if (step == 1) {
        result = this.substring (start, stop);
    }
    else {
        for (var index = start; index < stop; index += step) {
            result = result.concat (this.charAt(index));
        }
    }
    return result;
};
__setproperty__ (String.prototype, 'format', {
    get: function () {return __get__ (this, function (self) {
        var args = tuple ([] .slice.apply (arguments).slice (1));
        var autoIndex = 0;
        return self.replace (/\{(\w*)\}/g, function (match, key) {
            if (key == '') {
                key = autoIndex++;
            }
            if (key == +key) {
                return args [key] === undefined ? match : str (args [key]);
            }
            else {
                for (var index = 0; index < args.length; index++) {
                    if (typeof args [index] == 'object' && args [index][key] !== undefined) {
                        return str (args [index][key]);
                    }
                }
                return match;
            }
        });
    });},
    enumerable: true
});
String.prototype.isalnum = function () {
    return /^[0-9a-zA-Z]{1,}$/.test(this)
};
String.prototype.isalpha = function () {
    return /^[a-zA-Z]{1,}$/.test(this)
};
String.prototype.isdecimal = function () {
    return /^[0-9]{1,}$/.test(this)
};
String.prototype.isdigit = function () {
    return this.isdecimal()
};
String.prototype.islower = function () {
    return /^[a-z]{1,}$/.test(this)
};
String.prototype.isupper = function () {
    return /^[A-Z]{1,}$/.test(this)
};
String.prototype.isspace = function () {
    return /^[\s]{1,}$/.test(this)
};
String.prototype.isnumeric = function () {
    return !isNaN (parseFloat (this)) && isFinite (this);
};
String.prototype.join = function (strings) {
    strings = Array.from (strings);
    return strings.join (this);
};
String.prototype.lower = function () {
    return this.toLowerCase ();
};
String.prototype.py_replace = function (old, aNew, maxreplace) {
    return this.split (old, maxreplace) .join (aNew);
};
String.prototype.lstrip = function () {
    return this.replace (/^\s*/g, '');
};
String.prototype.rfind = function (sub, start) {
    return this.lastIndexOf (sub, start);
};
String.prototype.rsplit = function (sep, maxsplit) {
    if (sep == undefined || sep == null) {
        sep = /\s+/;
        var stripped = this.strip ();
    }
    else {
        var stripped = this;
    }
    if (maxsplit == undefined || maxsplit == -1) {
        return stripped.split (sep);
    }
    else {
        var result = stripped.split (sep);
        if (maxsplit < result.length) {
            var maxrsplit = result.length - maxsplit;
            return [result.slice (0, maxrsplit) .join (sep)] .concat (result.slice (maxrsplit));
        }
        else {
            return result;
        }
    }
};
String.prototype.rstrip = function () {
    return this.replace (/\s*$/g, '');
};
String.prototype.py_split = function (sep, maxsplit) {
    if (sep == undefined || sep == null) {
        sep = /\s+/;
        var stripped = this.strip ();
    }
    else {
        var stripped = this;
    }
    if (maxsplit == undefined || maxsplit == -1) {
        return stripped.split (sep);
    }
    else {
        var result = stripped.split (sep);
        if (maxsplit < result.length) {
            return result.slice (0, maxsplit).concat ([result.slice (maxsplit).join (sep)]);
        }
        else {
            return result;
        }
    }
};
String.prototype.startswith = function (prefix) {
    if (prefix instanceof Array) {
        for (var i=0;i<prefix.length;i++) {
            if (this.indexOf (prefix [i]) == 0)
                return true;
        }
    } else
        return this.indexOf (prefix) == 0;
    return false;
};
String.prototype.strip = function () {
    return this.trim ();
};
String.prototype.upper = function () {
    return this.toUpperCase ();
};
String.prototype.__mul__ = function (scalar) {
    var result = '';
    for (var i = 0; i < scalar; i++) {
        result = result + this;
    }
    return result;
};
String.prototype.__rmul__ = String.prototype.__mul__;
function __contains__ (element) {
    return this.hasOwnProperty (element);
}
function __keys__ () {
    var keys = [];
    for (var attrib in this) {
        if (!__specialattrib__ (attrib)) {
            keys.push (attrib);
        }
    }
    return keys;
}
function __items__ () {
    var items = [];
    for (var attrib in this) {
        if (!__specialattrib__ (attrib)) {
            items.push ([attrib, this [attrib]]);
        }
    }
    return items;
}
function __del__ (key) {
    delete this [key];
}
function __clear__ () {
    for (var attrib in this) {
        delete this [attrib];
    }
}
function __getdefault__ (aKey, aDefault) {
    var result = this [aKey];
    if (result == undefined) {
        result = this ['py_' + aKey];
    }
    return result == undefined ? (aDefault == undefined ? null : aDefault) : result;
}
function __setdefault__ (aKey, aDefault) {
    var result = this [aKey];
    if (result != undefined) {
        return result;
    }
    var val = aDefault == undefined ? null : aDefault;
    this [aKey] = val;
    return val;
}
function __pop__ (aKey, aDefault) {
    var result = this [aKey];
    if (result != undefined) {
        delete this [aKey];
        return result;
    } else {
        if ( aDefault === undefined ) {
            throw KeyError (aKey, new Error());
        }
    }
    return aDefault;
}
function __popitem__ () {
    var aKey = Object.keys (this) [0];
    if (aKey == null) {
        throw KeyError ("popitem(): dictionary is empty", new Error ());
    }
    var result = tuple ([aKey, this [aKey]]);
    delete this [aKey];
    return result;
}
function __update__ (aDict) {
    for (var aKey in aDict) {
        this [aKey] = aDict [aKey];
    }
}
function __values__ () {
    var values = [];
    for (var attrib in this) {
        if (!__specialattrib__ (attrib)) {
            values.push (this [attrib]);
        }
    }
    return values;
}
function __dgetitem__ (aKey) {
    return this [aKey];
}
function __dsetitem__ (aKey, aValue) {
    this [aKey] = aValue;
}
function dict (objectOrPairs) {
    var instance = {};
    if (!objectOrPairs || objectOrPairs instanceof Array) {
        if (objectOrPairs) {
            for (var index = 0; index < objectOrPairs.length; index++) {
                var pair = objectOrPairs [index];
                if ( !(pair instanceof Array) || pair.length != 2) {
                    throw ValueError(
                        "dict update sequence element #" + index +
                        " has length " + pair.length +
                        "; 2 is required", new Error());
                }
                var key = pair [0];
                var val = pair [1];
                if (!(objectOrPairs instanceof Array) && objectOrPairs instanceof Object) {
                     if (!isinstance (objectOrPairs, dict)) {
                         val = dict (val);
                     }
                }
                instance [key] = val;
            }
        }
    }
    else {
        if (isinstance (objectOrPairs, dict)) {
            var aKeys = objectOrPairs.py_keys ();
            for (var index = 0; index < aKeys.length; index++ ) {
                var key = aKeys [index];
                instance [key] = objectOrPairs [key];
            }
        } else if (objectOrPairs instanceof Object) {
            instance = objectOrPairs;
        } else {
            throw ValueError ("Invalid type of object for dict creation", new Error ());
        }
    }
    __setproperty__ (instance, '__class__', {value: dict, enumerable: false, writable: true});
    __setproperty__ (instance, '__contains__', {value: __contains__, enumerable: false});
    __setproperty__ (instance, 'py_keys', {value: __keys__, enumerable: false});
    __setproperty__ (instance, '__iter__', {value: function () {new __PyIterator__ (this.py_keys ());}, enumerable: false});
    __setproperty__ (instance, Symbol.iterator, {value: function () {new __JsIterator__ (this.py_keys ());}, enumerable: false});
    __setproperty__ (instance, 'py_items', {value: __items__, enumerable: false});
    __setproperty__ (instance, 'py_del', {value: __del__, enumerable: false});
    __setproperty__ (instance, 'py_clear', {value: __clear__, enumerable: false});
    __setproperty__ (instance, 'py_get', {value: __getdefault__, enumerable: false});
    __setproperty__ (instance, 'py_setdefault', {value: __setdefault__, enumerable: false});
    __setproperty__ (instance, 'py_pop', {value: __pop__, enumerable: false});
    __setproperty__ (instance, 'py_popitem', {value: __popitem__, enumerable: false});
    __setproperty__ (instance, 'py_update', {value: __update__, enumerable: false});
    __setproperty__ (instance, 'py_values', {value: __values__, enumerable: false});
    __setproperty__ (instance, '__getitem__', {value: __dgetitem__, enumerable: false});
    __setproperty__ (instance, '__setitem__', {value: __dsetitem__, enumerable: false});
    return instance;
}
dict.__name__ = 'dict';
dict.__bases__ = [object];
function __setdoc__ (docString) {
    this.__doc__ = docString;
    return this;
}
__setproperty__ (Function.prototype, '__setdoc__', {value: __setdoc__, enumerable: false});
function __mod__ (a, b) {
    if (typeof a == 'object' && '__mod__' in a) {
        return a.__mod__ (b);
    }
    else if (typeof b == 'object' && '__rmod__' in b) {
        return b.__rmod__ (a);
    }
    else {
        return ((a % b) + b) % b;
    }
}function __neg__ (a) {
    if (typeof a == 'object' && '__neg__' in a) {
        return a.__neg__ ();
    }
    else {
        return -a;
    }
}function __add__ (a, b) {
    if (typeof a == 'object' && '__add__' in a) {
        return a.__add__ (b);
    }
    else if (typeof b == 'object' && '__radd__' in b) {
        return b.__radd__ (a);
    }
    else {
        return a + b;
    }
}function __eq__ (a, b) {
    if (typeof a == 'object' && '__eq__' in a) {
        return a.__eq__ (b);
    }
    else {
        return a == b;
    }
}function __iadd__ (a, b) {
    if (typeof a == 'object' && '__iadd__' in a) {
        return a.__iadd__ (b);
    }
    else if (typeof a == 'object' && '__add__' in a) {
        return a = a.__add__ (b);
    }
    else if (typeof b == 'object' && '__radd__' in b) {
        return a = b.__radd__ (a);
    }
    else {
        return a += b;
    }
}function __getitem__ (container, key) {
    if (typeof container == 'object' && '__getitem__' in container) {
        return container.__getitem__ (key);
    }
    else if ((typeof container == 'string' || container instanceof Array) && key < 0) {
        return container [container.length + key];
    }
    else {
        return container [key];
    }
}var BaseException =  __class__ ('BaseException', [object], {
	__module__: __name__,
});
var Exception =  __class__ ('Exception', [BaseException], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		var kwargs = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete kwargs.__kwargtrans__;
			}
			var args = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
		}
		else {
			var args = tuple ();
		}
		self.__args__ = args;
		try {
			self.stack = kwargs.error.stack;
		}
		catch (__except0__) {
			self.stack = 'No stack trace available';
		}
	});},
	get __repr__ () {return __get__ (this, function (self) {
		if (len (self.__args__) > 1) {
			return '{}{}'.format (self.__class__.__name__, repr (tuple (self.__args__)));
		}
		else if (len (self.__args__)) {
			return '{}({})'.format (self.__class__.__name__, repr (self.__args__ [0]));
		}
		else {
			return '{}()'.format (self.__class__.__name__);
		}
	});},
	get __str__ () {return __get__ (this, function (self) {
		if (len (self.__args__) > 1) {
			return str (tuple (self.__args__));
		}
		else if (len (self.__args__)) {
			return str (self.__args__ [0]);
		}
		else {
			return '';
		}
	});}
});
var IterableError =  __class__ ('IterableError', [Exception], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, error) {
		Exception.__init__ (self, "Can't iterate over non-iterable", __kwargtrans__ ({error: error}));
	});}
});
var StopIteration =  __class__ ('StopIteration', [Exception], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, error) {
		Exception.__init__ (self, 'Iterator exhausted', __kwargtrans__ ({error: error}));
	});}
});
var ValueError =  __class__ ('ValueError', [Exception], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, message, error) {
		Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
	});}
});
var KeyError =  __class__ ('KeyError', [Exception], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, message, error) {
		Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
	});}
});
var AssertionError =  __class__ ('AssertionError', [Exception], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, message, error) {
		if (message) {
			Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
		}
		else {
			Exception.__init__ (self, __kwargtrans__ ({error: error}));
		}
	});}
});
var NotImplementedError =  __class__ ('NotImplementedError', [Exception], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, message, error) {
		Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
	});}
});
var IndexError =  __class__ ('IndexError', [Exception], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, message, error) {
		Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
	});}
});
var AttributeError =  __class__ ('AttributeError', [Exception], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, message, error) {
		Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
	});}
});
var py_TypeError =  __class__ ('py_TypeError', [Exception], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, message, error) {
		Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
	});}
});
var Warning =  __class__ ('Warning', [Exception], {
	__module__: __name__,
});
var UserWarning =  __class__ ('UserWarning', [Warning], {
	__module__: __name__,
});
var DeprecationWarning =  __class__ ('DeprecationWarning', [Warning], {
	__module__: __name__,
});
var RuntimeWarning =  __class__ ('RuntimeWarning', [Warning], {
	__module__: __name__,
});
var __sort__ = function (iterable, key, reverse) {
	if (typeof key == 'undefined' || (key != null && key.hasOwnProperty ("__kwargtrans__"))) {		var key = null;
	}	if (typeof reverse == 'undefined' || (reverse != null && reverse.hasOwnProperty ("__kwargtrans__"))) {		var reverse = false;
	}	if (arguments.length) {
		var __ilastarg0__ = arguments.length - 1;
		if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
			var __allkwargs0__ = arguments [__ilastarg0__--];
			for (var __attrib0__ in __allkwargs0__) {
				switch (__attrib0__) {
					case 'iterable': var iterable = __allkwargs0__ [__attrib0__]; break;
					case 'key': var key = __allkwargs0__ [__attrib0__]; break;
					case 'reverse': var reverse = __allkwargs0__ [__attrib0__]; break;
				}
			}
		}
	}
	if (key) {
		iterable.sort ((function __lambda__ (a, b) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'a': var a = __allkwargs0__ [__attrib0__]; break;
							case 'b': var b = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			return (key (a) > key (b) ? 1 : -(1));
		}));
	}
	else {
		iterable.sort ();
	}
	if (reverse) {
		iterable.reverse ();
	}
};
var divmod = function (n, d) {
	return tuple ([Math.floor (n / d), __mod__ (n, d)]);
};
var __Terminal__ =  __class__ ('__Terminal__', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		self.buffer = '';
		try {
			self.element = document.getElementById ('__terminal__');
		}
		catch (__except0__) {
			self.element = null;
		}
		if (self.element) {
			self.element.style.overflowX = 'auto';
			self.element.style.boxSizing = 'border-box';
			self.element.style.padding = '5px';
			self.element.innerHTML = '_';
		}
	});},
	get print () {return __get__ (this, function (self) {
		var sep = ' ';
		var end = '\n';
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'sep': var sep = __allkwargs0__ [__attrib0__]; break;
						case 'end': var end = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
			var args = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
		}
		else {
			var args = tuple ();
		}
		self.buffer = '{}{}{}'.format (self.buffer, sep.join ((function () {
			var __accu0__ = [];
			for (var arg of args) {
				__accu0__.append (str (arg));
			}
			return __accu0__;
		}) ()), end).__getslice__ (-(4096), null, 1);
		if (self.element) {
			self.element.innerHTML = self.buffer.py_replace ('\n', '<br>').py_replace (' ', '&nbsp');
			self.element.scrollTop = self.element.scrollHeight;
		}
		else {
			console.log (sep.join ((function () {
				var __accu0__ = [];
				for (var arg of args) {
					__accu0__.append (str (arg));
				}
				return __accu0__;
			}) ()));
		}
	});},
	get input () {return __get__ (this, function (self, question) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'question': var question = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		self.print ('{}'.format (question), __kwargtrans__ ({end: ''}));
		var answer = window.prompt ('\n'.join (self.buffer.py_split ('\n').__getslice__ (-(8), null, 1)));
		self.print (answer);
		return answer;
	});}
});
var __terminal__ = __Terminal__ ();
var print = __terminal__.print;
var input = __terminal__.input;

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var __name__$1 = 'battlecode';
var SPECS = dict ({'COMMUNICATION_BITS': 16, 'CASTLE_TALK_BITS': 8, 'MAX_ROUNDS': 1000, 'TRICKLE_FUEL': 25, 'INITIAL_KARBONITE': 100, 'INITIAL_FUEL': 500, 'MINE_FUEL_COST': 1, 'KARBONITE_YIELD': 2, 'FUEL_YIELD': 10, 'MAX_TRADE': 1024, 'MAX_BOARD_SIZE': 64, 'MAX_ID': 4096, 'CASTLE': 0, 'CHURCH': 1, 'PILGRIM': 2, 'CRUSADER': 3, 'PROPHET': 4, 'PREACHER': 5, 'RED': 0, 'BLUE': 1, 'CHESS_INITIAL': 100, 'CHESS_EXTRA': 20, 'TURN_MAX_TIME': 200, 'MAX_MEMORY': 50000000, 'UNITS': [dict ({'CONSTRUCTION_KARBONITE': null, 'CONSTRUCTION_FUEL': null, 'KARBONITE_CAPACITY': null, 'FUEL_CAPACITY': null, 'SPEED': 0, 'FUEL_PER_MOVE': null, 'STARTING_HP': 100, 'VISION_RADIUS': 100, 'ATTACK_DAMAGE': null, 'ATTACK_RADIUS': null, 'ATTACK_FUEL_COST': null, 'DAMAGE_SPREAD': null}), dict ({'CONSTRUCTION_KARBONITE': 50, 'CONSTRUCTION_FUEL': 200, 'KARBONITE_CAPACITY': null, 'FUEL_CAPACITY': null, 'SPEED': 0, 'FUEL_PER_MOVE': null, 'STARTING_HP': 50, 'VISION_RADIUS': 100, 'ATTACK_DAMAGE': null, 'ATTACK_RADIUS': null, 'ATTACK_FUEL_COST': null, 'DAMAGE_SPREAD': null}), dict ({'CONSTRUCTION_KARBONITE': 10, 'CONSTRUCTION_FUEL': 50, 'KARBONITE_CAPACITY': 20, 'FUEL_CAPACITY': 100, 'SPEED': 4, 'FUEL_PER_MOVE': 1, 'STARTING_HP': 10, 'VISION_RADIUS': 100, 'ATTACK_DAMAGE': null, 'ATTACK_RADIUS': null, 'ATTACK_FUEL_COST': null, 'DAMAGE_SPREAD': null}), dict ({'CONSTRUCTION_KARBONITE': 20, 'CONSTRUCTION_FUEL': 50, 'KARBONITE_CAPACITY': 20, 'FUEL_CAPACITY': 100, 'SPEED': 9, 'FUEL_PER_MOVE': 1, 'STARTING_HP': 40, 'VISION_RADIUS': 36, 'ATTACK_DAMAGE': 10, 'ATTACK_RADIUS': [1, 16], 'ATTACK_FUEL_COST': 10, 'DAMAGE_SPREAD': 0}), dict ({'CONSTRUCTION_KARBONITE': 25, 'CONSTRUCTION_FUEL': 50, 'KARBONITE_CAPACITY': 20, 'FUEL_CAPACITY': 100, 'SPEED': 4, 'FUEL_PER_MOVE': 2, 'STARTING_HP': 20, 'VISION_RADIUS': 64, 'ATTACK_DAMAGE': 10, 'ATTACK_RADIUS': [16, 64], 'ATTACK_FUEL_COST': 25, 'DAMAGE_SPREAD': 0}), dict ({'CONSTRUCTION_KARBONITE': 30, 'CONSTRUCTION_FUEL': 50, 'KARBONITE_CAPACITY': 20, 'FUEL_CAPACITY': 100, 'SPEED': 4, 'FUEL_PER_MOVE': 3, 'STARTING_HP': 60, 'VISION_RADIUS': 16, 'ATTACK_DAMAGE': 20, 'ATTACK_RADIUS': [1, 16], 'ATTACK_FUEL_COST': 15, 'DAMAGE_SPREAD': 3})]});
var BCAbstractRobot =  __class__ ('BCAbstractRobot', [object], {
	__module__: __name__$1,
	get __init__ () {return __get__ (this, function (self) {
		self._bc_reset_state ();
	});},
	get _do_turn () {return __get__ (this, function (self, game_state) {
		self._bc_game_state = game_state;
		self.id = game_state ['id'];
		self.karbonite = game_state ['karbonite'];
		self.fuel = game_state ['fuel'];
		self.last_offer = game_state ['last_offer'];
		self.me = self.get_robot (self.id);
		if (self.me.turn == 1) {
			self.map = game_state ['map'];
			self.karbonite_map = game_state ['karbonite_map'];
			self.fuel_map = game_state ['fuel_map'];
		}
		try {
			var t = self.turn ();
		}
		catch (__except0__) {
			if (isinstance (__except0__, Exception)) {
				var e = __except0__;
				var t = self._bc_error_action (e);
			}
			else {
				throw __except0__;
			}
		}
		if (!(t)) {
			var t = self._bc_null_action ();
		}
		t ['signal'] = self._bc_signal;
		t ['signal_radius'] = self._bc_signal_radius;
		t ['logs'] = self._bc_logs;
		t ['castle_talk'] = self._bc_castle_talk;
		self._bc_reset_state ();
		return t;
	});},
	get _bc_reset_state () {return __get__ (this, function (self) {
		self._bc_logs = [];
		self._bc_signal = 0;
		self._bc_signal_radius = 0;
		self._bc_game_state = null;
		self._bc_castle_talk = 0;
		self.me = null;
		self.id = null;
		self.fuel = null;
		self.karbonite = null;
		self.last_offer = null;
	});},
	get _bc_null_action () {return __get__ (this, function (self) {
		return dict ({'signal': self._bc_signal, 'signal_radius': self._bc_signal_radius, 'logs': self._bc_logs, 'castle_talk': self._bc_castle_talk});
	});},
	get _bc_error_action () {return __get__ (this, function (self, e) {
		var a = self._bc_null_action ();
		a ['error'] = str (e);
		return a;
	});},
	get _bc_action () {return __get__ (this, function (self, action, properties) {
		if (typeof properties == 'undefined' || (properties != null && properties.hasOwnProperty ("__kwargtrans__"))) {			var properties = null;
		}		var a = self._bc_null_action ();
		if (properties) {
			for (var key of properties.py_keys ()) {
				a [key] = properties [key];
			}
		}
		a ['action'] = action;
		return a;
	});},
	get _bc_check_on_map () {return __get__ (this, function (self, x, y) {
		return x >= 0 && x < len (self._bc_game_state ['shadow'] [0]) && y >= 0 && y < len (self._bc_game_state ['shadow']);
	});},
	get log () {return __get__ (this, function (self, message) {
		self._bc_logs.append (str (message));
	});},
	get signal () {return __get__ (this, function (self, value, radius) {
		if (self.fuel < radius) {
			var __except0__ = Exception ('Not enough fuel to signal given radius.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (value < 0 || value >= Math.pow (2, SPECS ['COMMUNICATION_BITS'])) {
			var __except0__ = Exception ('Invalid signal, must be int within bit range.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (radius > 2 * Math.pow (SPECS ['MAX_BOARD_SIZE'] - 1, 2)) {
			var __except0__ = Exception ('Signal radius is too big.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		self._bc_signal = value;
		self._bc_signal_radius = radius;
		self.fuel -= radius;
	});},
	get castle_talk () {return __get__ (this, function (self, value) {
		if (value < 0 || value >= Math.pow (2, SPECS ['CASTLE_TALK_BITS'])) {
			var __except0__ = Exception ('Invalid castle talk, must be between 0 and 2^8.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		self._bc_castle_talk = value;
	});},
	get propose_trade () {return __get__ (this, function (self, karbonite, fuel) {
		if (self.me ['unit'] != SPECS ['CASTLE']) {
			var __except0__ = Exception ('Only castles can trade.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (abs (karbonite) >= SPECS ['MAX_TRADE'] || abs (fuel) >= SPECS ['MAX_TRADE']) {
			var __except0__ = Exception (('Cannot trade over ' + str (SPECS ['MAX_TRADE'])) + ' in a given turn.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		return self._bc_action ('trade', dict ({'trade_fuel': fuel, 'trade_karbonite': karbonite}));
	});},
	get build_unit () {return __get__ (this, function (self, unit, dx, dy) {
		if (self.me ['unit'] != SPECS ['PILGRIM'] && self.me ['unit'] != SPECS ['CASTLE'] && self.me ['unit'] != SPECS ['CHURCH']) {
			var __except0__ = Exception ('This unit type cannot build.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self.me ['unit'] == SPECS ['PILGRIM'] && unit != SPECS ['CHURCH']) {
			var __except0__ = Exception ('Pilgrims can only build churches.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self.me ['unit'] != SPECS ['PILGRIM'] && unit == SPECS ['CHURCH']) {
			var __except0__ = Exception ('Only pilgrims can build churches.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (dx < -(1) || dy < -(1) || dx > 1 || dy > 1) {
			var __except0__ = Exception ('Can only build in adjacent squares.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (!(self._bc_check_on_map (self.me ['x'] + dx, self.me ['y'] + dy))) {
			var __except0__ = Exception ("Can't build units off of map.");
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self._bc_game_state ['shadow'] [self.me ['y'] + dy] [self.me ['x'] + dx] != 0) {
			var __except0__ = Exception ('Cannot build on occupied tile.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (!(self.map [self.me ['y'] + dy] [self.me ['x'] + dx])) {
			var __except0__ = Exception ('Cannot build onto impassable terrain.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self.karbonite < SPECS ['UNITS'] [unit] ['CONSTRUCTION_KARBONITE'] || self.fuel < SPECS ['UNITS'] [unit] ['CONSTRUCTION_FUEL']) {
			var __except0__ = Exception ('Cannot afford to build specified unit.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		return self._bc_action ('build', dict ({'dx': dx, 'dy': dy, 'build_unit': unit}));
	});},
	get move () {return __get__ (this, function (self, dx, dy) {
		if (self.me ['unit'] == SPECS ['CASTLE'] || self.me ['unit'] == SPECS ['CHURCH']) {
			var __except0__ = Exception ('Churches and Castles cannot move.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (!(self._bc_check_on_map (self.me ['x'] + dx, self.me ['y'] + dy))) {
			var __except0__ = Exception ("Can't move off of map.");
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self._bc_game_state.shadow [self.me ['y'] + dy] [self.me ['x'] + dx] == -(1)) {
			var __except0__ = Exception ('Cannot move outside of vision range.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self._bc_game_state.shadow [self.me ['y'] + dy] [self.me ['x'] + dx] != 0) {
			var __except0__ = Exception ('Cannot move onto occupied tile.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (!(self.map [self.me ['y'] + dy] [self.me ['x'] + dx])) {
			var __except0__ = Exception ('Cannot move onto impassable terrain.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		var r = Math.pow (dx, 2) + Math.pow (dy, 2);
		if (r > SPECS ['UNITS'] [self.me ['unit']] ['SPEED']) {
			var __except0__ = Exception ('Slow down, cowboy.  Tried to move faster than unit can.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self.fuel < r * SPECS ['UNITS'] [self.me ['unit']] ['FUEL_PER_MOVE']) {
			var __except0__ = Exception ('Not enough fuel to move at given speed.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		return self._bc_action ('move', dict ({'dx': dx, 'dy': dy}));
	});},
	get mine () {return __get__ (this, function (self) {
		if (self.me ['unit'] != SPECS ['PILGRIM']) {
			var __except0__ = Exception ('Only Pilgrims can mine.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self.fuel < SPECS ['MINE_FUEL_COST']) {
			var __except0__ = Exception ('Not enough fuel to mine.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self.karbonite_map [self.me ['y']] [self.me ['x']]) {
			if (self.me ['karbonite'] >= SPECS ['UNITS'] [SPECS ['PILGRIM']] ['KARBONITE_CAPACITY']) {
				var __except0__ = Exception ('Cannot mine, as at karbonite capacity.');
				__except0__.__cause__ = null;
				throw __except0__;
			}
		}
		else if (self.fuel_map [self.me ['y']] [self.me ['x']]) {
			if (self.me ['fuel'] >= SPECS ['UNITS'] [SPECS ['PILGRIM']] ['FUEL_CAPACITY']) {
				var __except0__ = Exception ('Cannot mine, as at fuel capacity.');
				__except0__.__cause__ = null;
				throw __except0__;
			}
		}
		else {
			var __except0__ = Exception ('Cannot mine square without fuel or karbonite.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		return self._bc_action ('mine');
	});},
	get give () {return __get__ (this, function (self, dx, dy, karbonite, fuel) {
		if (dx > 1 || dx < -(1) || dy > 1 || dy < -(1) || dx == 0 && dy == 0) {
			var __except0__ = Exception ('Can only give to adjacent squares.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (!(self._bc_check_on_map (self.me ['x'] + dx, self.me ['y'] + dy))) {
			var __except0__ = Exception ("Can't give off of map.");
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self._bc_game_state ['shadow'] [self.me ['y'] + dy] [self.me ['x'] + dx] <= 0) {
			var __except0__ = Exception ('Cannot give to empty square.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (karbonite < 0 || fuel < 0 || self.me ['karbonite'] < karbonite || self.me ['fuel'] < fuel) {
			var __except0__ = Exception ('Do not have specified amount to give.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		return self._bc_action ('give', dict ({'dx': dx, 'dy': dy, 'give_karbonite': karbonite, 'give_fuel': fuel}));
	});},
	get attack () {return __get__ (this, function (self, dx, dy) {
		if (self.me ['unit'] != SPECS ['CRUSADER'] && self.me ['unit'] != SPECS ['PREACHER'] && self.me ['unit'] != SPECS ['PROPHET']) {
			var __except0__ = Exception ('Given unit cannot attack.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self.fuel < SPECS ['UNITS'] [self.me ['unit']] ['ATTACK_FUEL_COST']) {
			var __except0__ = Exception ('Not enough fuel to attack.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (!(self._bc_check_on_map (self.me ['x'] + dx, self.me ['y'] + dy))) {
			var __except0__ = Exception ("Can't attack off of map.");
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (self._bc_game_state ['shadow'] [self.me ['y'] + dy] [self.me ['x'] + dx] == -(1)) {
			var __except0__ = Exception ('Cannot attack outside of vision range.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (!(self.map [self.me ['y'] + dy] [self.me ['x'] + dx])) {
			var __except0__ = Exception ('Cannot attack impassable terrain.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		var r = Math.pow (dx, 2) + Math.pow (dy, 2);
		if (r > SPECS ['UNITS'] [self.me ['unit']] ['ATTACK_RADIUS'] [1] || r < SPECS ['UNITS'] [self.me ['unit']] ['ATTACK_RADIUS'] [0]) {
			var __except0__ = Exception ('Cannot attack outside of attack range.');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		return self._bc_action ('attack', dict ({'dx': dx, 'dy': dy}));
	});},
	get get_robot () {return __get__ (this, function (self, id) {
		if (id <= 0) {
			return null;
		}
		for (var robot of self._bc_game_state ['visible']) {
			if (robot ['id'] == id) {
				return robot;
			}
		}
		return null;
	});},
	get is_visible () {return __get__ (this, function (self, robot) {
		var x = __in__ ('x', robot);
		return x;
	});},
	get is_radioing () {return __get__ (this, function (self, robot) {
		return robot ['signal'] >= 0;
	});},
	get get_visible_robot_map () {return __get__ (this, function (self) {
		return self._bc_game_state ['shadow'];
	});},
	get get_passable_map () {return __get__ (this, function (self) {
		return self.map;
	});},
	get get_karbonite_map () {return __get__ (this, function (self) {
		return self.karbonite_map;
	});},
	get get_fuel_map () {return __get__ (this, function (self) {
		return self.fuel_map;
	});},
	get get_visible_robots () {return __get__ (this, function (self) {
		return self._bc_game_state ['visible'];
	});},
	get turn () {return __get__ (this, function (self) {
		return null;
	});}
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var pathfinding_heuristic_multiplier = 1.1;
var pilgrim_will_scavenge_closeby_mines_before_turns = 10;
var pilgrim_will_scavenge_closeby_mines = 50;
var chokepoint_modifier = 0.4;
var karbonite_modifier = 0.05;
var fuel_modifier = 0.05;
var directions = [tuple ([-(1), 0]), tuple ([-(1), 1]), tuple ([0, 1]), tuple ([1, 1]), tuple ([1, 0]), tuple ([1, -(1)]), tuple ([0, -(1)]), tuple ([-(1), -(1)])];
var crusader_move_directions = [tuple ([0, 1]), tuple ([0, -(1)]), tuple ([1, 0]), tuple ([-(1), 0]), tuple ([-(1), 1]), tuple ([1, 1]), tuple ([1, -(1)]), tuple ([-(1), -(1)]), tuple ([0, 2]), tuple ([0, -(2)]), tuple ([2, 0]), tuple ([-(2), 0]), tuple ([-(1), 2]), tuple ([1, 2]), tuple ([1, -(2)]), tuple ([-(1), -(2)]), tuple ([2, -(1)]), tuple ([2, 1]), tuple ([-(2), 1]), tuple ([-(2), -(1)]), tuple ([2, 2]), tuple ([2, -(2)]), tuple ([-(2), 2]), tuple ([-(2), -(2)]), tuple ([0, 3]), tuple ([0, -(3)]), tuple ([3, 0]), tuple ([-(3), 0])];
var non_crusader_move_directions = [tuple ([0, 1]), tuple ([0, -(1)]), tuple ([1, 0]), tuple ([-(1), 0]), tuple ([-(1), 1]), tuple ([1, 1]), tuple ([1, -(1)]), tuple ([-(1), -(1)]), tuple ([0, 2]), tuple ([0, -(2)]), tuple ([2, 0]), tuple ([-(2), 0])];
var enemy_unit_priority_for_prophet = [2, 2, 3, 4, 4, 10];
var unit_castle = SPECS ['CASTLE'];
var unit_church = SPECS ['CHURCH'];
var unit_crusader = SPECS ['CRUSADER'];
var unit_pilgrim = SPECS ['PILGRIM'];
var unit_preacher = SPECS ['PREACHER'];
var unit_prophet = SPECS ['PROPHET'];
var crusader_attack_damage = SPECS ['UNITS'] [SPECS ['CRUSADER']] ['ATTACK_DAMAGE'];
var prophet_attack_damage = SPECS ['UNITS'] [SPECS ['PROPHET']] ['ATTACK_DAMAGE'];
var preacher_attack_damage = SPECS ['UNITS'] [SPECS ['PREACHER']] ['ATTACK_DAMAGE'];
var crusader_min_attack_range = SPECS ['UNITS'] [SPECS ['CRUSADER']] ['ATTACK_RADIUS'] [0];
var crusader_max_attack_range = SPECS ['UNITS'] [SPECS ['CRUSADER']] ['ATTACK_RADIUS'] [1];
var prophet_min_attack_range = SPECS ['UNITS'] [SPECS ['PROPHET']] ['ATTACK_RADIUS'] [0];
var prophet_max_attack_range = SPECS ['UNITS'] [SPECS ['PROPHET']] ['ATTACK_RADIUS'] [1];
var preacher_min_attack_range = SPECS ['UNITS'] [SPECS ['PREACHER']] ['ATTACK_RADIUS'] [0];
var preacher_max_attack_range = SPECS ['UNITS'] [SPECS ['PREACHER']] ['ATTACK_RADIUS'] [1];
var castle_max_health = SPECS ['UNITS'] [SPECS ['CASTLE']] ['STARTING_HP'];
var church_max_health = SPECS ['UNITS'] [SPECS ['CHURCH']] ['STARTING_HP'];
var pilgrim_max_health = SPECS ['UNITS'] [SPECS ['PILGRIM']] ['STARTING_HP'];
var crusader_max_health = SPECS ['UNITS'] [SPECS ['CRUSADER']] ['STARTING_HP'];
var prophet_max_health = SPECS ['UNITS'] [SPECS ['PROPHET']] ['STARTING_HP'];
var preacher_max_health = SPECS ['UNITS'] [SPECS ['PREACHER']] ['STARTING_HP'];
var pilgrim_will_scavenge_closeby_mines_after_turns = 50;
var get_required_constant = function () {
};
var pilgrim_directions = [null, tuple ([0, 0]), tuple ([0, 1]), tuple ([0, 2]), tuple ([0, -(1)]), tuple ([0, -(2)]), tuple ([-(1), 0]), tuple ([-(2), 0]), tuple ([1, 0]), tuple ([2, 0]), tuple ([-(1), 1]), tuple ([-(1), -(1)]), tuple ([1, -(1)]), tuple ([1, 1])];

var __module_constants__ = /*#__PURE__*/Object.freeze({
    pathfinding_heuristic_multiplier: pathfinding_heuristic_multiplier,
    pilgrim_will_scavenge_closeby_mines_before_turns: pilgrim_will_scavenge_closeby_mines_before_turns,
    pilgrim_will_scavenge_closeby_mines: pilgrim_will_scavenge_closeby_mines,
    chokepoint_modifier: chokepoint_modifier,
    karbonite_modifier: karbonite_modifier,
    fuel_modifier: fuel_modifier,
    directions: directions,
    crusader_move_directions: crusader_move_directions,
    non_crusader_move_directions: non_crusader_move_directions,
    enemy_unit_priority_for_prophet: enemy_unit_priority_for_prophet,
    unit_castle: unit_castle,
    unit_church: unit_church,
    unit_crusader: unit_crusader,
    unit_pilgrim: unit_pilgrim,
    unit_preacher: unit_preacher,
    unit_prophet: unit_prophet,
    crusader_attack_damage: crusader_attack_damage,
    prophet_attack_damage: prophet_attack_damage,
    preacher_attack_damage: preacher_attack_damage,
    crusader_min_attack_range: crusader_min_attack_range,
    crusader_max_attack_range: crusader_max_attack_range,
    prophet_min_attack_range: prophet_min_attack_range,
    prophet_max_attack_range: prophet_max_attack_range,
    preacher_min_attack_range: preacher_min_attack_range,
    preacher_max_attack_range: preacher_max_attack_range,
    castle_max_health: castle_max_health,
    church_max_health: church_max_health,
    pilgrim_max_health: pilgrim_max_health,
    crusader_max_health: crusader_max_health,
    prophet_max_health: prophet_max_health,
    preacher_max_health: preacher_max_health,
    pilgrim_will_scavenge_closeby_mines_after_turns: pilgrim_will_scavenge_closeby_mines_after_turns,
    get_required_constant: get_required_constant,
    pilgrim_directions: pilgrim_directions
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var pi = Math.PI;
var e = Math.E;
var exp = Math.exp;
var expm1 = function (x) {
	return Math.exp (x) - 1;
};
var log = function (x, base) {
	return (base === undefined ? Math.log (x) : Math.log (x) / Math.log (base));
};
var log1p = function (x) {
	return Math.log (x + 1);
};
var log2 = function (x) {
	return Math.log (x) / Math.LN2;
};
var log10 = function (x) {
	return Math.log (x) / Math.LN10;
};
var pow$1 = Math.pow;
var sqrt = Math.sqrt;
var sin = Math.sin;
var cos = Math.cos;
var tan = Math.tan;
var asin = Math.asin;
var acos = Math.acos;
var atan = Math.atan;
var atan2 = Math.atan2;
var hypot = Math.hypot;
var degrees = function (x) {
	return (x * 180) / Math.PI;
};
var radians = function (x) {
	return (x * Math.PI) / 180;
};
var sinh = Math.sinh;
var cosh = Math.cosh;
var tanh = Math.tanh;
var asinh = Math.asinh;
var acosh = Math.acosh;
var atanh = Math.atanh;
var floor = Math.floor;
var ceil = Math.ceil;
var trunc = Math.trunc;
var isnan = isNaN;
var inf = Infinity;
var nan = NaN;
var modf = function (n) {
	var sign = (n >= 0 ? 1 : -(1));
	var __left0__ = divmod (abs (n), 1);
	var f = __left0__ [0];
	var mod = __left0__ [1];
	return tuple ([mod * sign, f * sign]);
};

var __module_math__ = /*#__PURE__*/Object.freeze({
    pi: pi,
    e: e,
    exp: exp,
    expm1: expm1,
    log: log,
    log1p: log1p,
    log2: log2,
    log10: log10,
    pow: pow$1,
    sqrt: sqrt,
    sin: sin,
    cos: cos,
    tan: tan,
    asin: asin,
    acos: acos,
    atan: atan,
    atan2: atan2,
    hypot: hypot,
    degrees: degrees,
    radians: radians,
    sinh: sinh,
    cosh: cosh,
    tanh: tanh,
    asinh: asinh,
    acosh: acosh,
    atanh: atanh,
    floor: floor,
    ceil: ceil,
    trunc: trunc,
    isnan: isnan,
    inf: inf,
    nan: nan,
    modf: modf
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var math = {};
__nest__ (math, '', __module_math__);
var _array = (function () {
	var __accu0__ = [];
	for (var i = 0; i < 624; i++) {
		__accu0__.append (0);
	}
	return __accu0__;
}) ();
var _index = 0;
var _bitmask1 = Math.pow (2, 32) - 1;
var _bitmask2 = Math.pow (2, 31);
var _bitmask3 = Math.pow (2, 31) - 1;
var _fill_array = function () {
	for (var i = 0; i < 624; i++) {
		var y = (_array [i] & _bitmask2) + (_array [__mod__ (i + 1, 624)] & _bitmask3);
		_array [i] = _array [__mod__ (i + 397, 624)] ^ y >> 1;
		if (__mod__ (y, 2) != 0) {
			_array [i] ^= 2567483615;
		}
	}
};
var _random_integer = function () {
	if (_index == 0) {
		_fill_array ();
	}
	var y = _array [_index];
	y ^= y >> 11;
	y ^= y << 7 & 2636928640;
	y ^= y << 15 & 4022730752;
	y ^= y >> 18;
	_index = __mod__ (_index + 1, 624);
	return y;
};
var seed = function (x) {
	if (typeof x == 'undefined' || (x != null && x.hasOwnProperty ("__kwargtrans__"))) {		var x = int (_bitmask3 * Math.random ());
	}	_array [0] = x;
	for (var i = 1; i < 624; i++) {
		_array [i] = (1812433253 * _array [i - 1] ^ (_array [i - 1] >> 30) + i) & _bitmask1;
	}
};
var randint = function (a, b) {
	return a + __mod__ (_random_integer (), (b - a) + 1);
};
var choice = function (seq) {
	return seq [randint (0, len (seq) - 1)];
};
var random = function () {
	return _random_integer () / _bitmask3;
};
var shuffle = function (x) {
	for (var i = len (x) - 1; i > 0; i--) {
		var j = math.floor (random () * (i + 1));
		var temp = x [i];
		x [i] = x [j];
		x [j] = temp;
	}
};
seed ();

var __module_random__ = /*#__PURE__*/Object.freeze({
    _array: _array,
    get _index () { return _index; },
    _bitmask1: _bitmask1,
    _bitmask2: _bitmask2,
    _bitmask3: _bitmask3,
    _fill_array: _fill_array,
    _random_integer: _random_integer,
    seed: seed,
    randint: randint,
    choice: choice,
    random: random,
    shuffle: shuffle
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var constants = {};
var random$1 = {};
__nest__ (constants, '', __module_constants__);
__nest__ (random$1, '', __module_random__);
var is_out_of_bounds = function (map_dim, pos_x, pos_y) {
	return pos_x < 0 || pos_y < 0 || pos_x >= map_dim || pos_y >= map_dim;
};
var is_cell_occupied = function (occupied_map, pos_x, pos_y) {
	var bounds_map = len (occupied_map);
	if (is_out_of_bounds (bounds_map, pos_x, pos_y)) {
		return true;
	}
	else if (occupied_map [pos_y] [pos_x] <= 0) {
		return false;
	}
	else {
		return true;
	}
};
var random_cells_around = function () {
	var dirs = constants.directions;
	random$1.shuffle (dirs, random$1.random);
	return dirs;
};
var get_relative_karbonite_mine_positions = function (robot) {
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var karb_map = robot.get_karbonite_map ();
	var map_length = len (karb_map);
	var queue = [];
	var distance = [];
	for (var iter_i = 0; iter_i < map_length; iter_i++) {
		for (var iter_j = 0; iter_j < map_length; iter_j++) {
			if (karb_map [iter_i] [iter_j]) {
				distance.append (Math.pow (iter_j - pos_x, 2) + Math.pow (iter_i - pos_y, 2));
				queue.append (tuple ([iter_j, iter_i]));
			}
		}
	}
	var __left0__ = insertionSort (distance, queue);
	var sorted_distance = __left0__ [0];
	var sorted_tuple = __left0__ [1];
	return tuple ([sorted_distance, sorted_tuple]);
};
var get_relative_fuel_mine_positions = function (robot) {
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var fuel_map = robot.get_fuel_map ();
	var map_length = len (fuel_map);
	var queue = [];
	var distance = [];
	for (var iter_i = 0; iter_i < map_length; iter_i++) {
		for (var iter_j = 0; iter_j < map_length; iter_j++) {
			if (fuel_map [iter_i] [iter_j]) {
				distance.append (Math.pow (iter_j - pos_x, 2) + Math.pow (iter_i - pos_y, 2));
				queue.append (tuple ([iter_j, iter_i]));
			}
		}
	}
	var __left0__ = insertionSort (distance, queue);
	var sorted_distance = __left0__ [0];
	var sorted_tuple = __left0__ [1];
	return tuple ([sorted_distance, sorted_tuple]);
};
var get_relative_mine_positions = function (robot) {
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var fuel_map = robot.get_fuel_map ();
	var karb_map = robot.get_karbonite_map ();
	var map_length = len (fuel_map);
	var queue = [];
	var distance = [];
	for (var iter_i = 0; iter_i < map_length; iter_i++) {
		for (var iter_j = 0; iter_j < map_length; iter_j++) {
			if (fuel_map [iter_i] [iter_j] || karb_map [iter_i] [iter_j]) {
				distance.append (Math.pow (iter_j - pos_x, 2) + Math.pow (iter_i - pos_y, 2));
				queue.append (tuple ([iter_j, iter_i]));
			}
		}
	}
	var __left0__ = insertionSort (distance, queue);
	var sorted_distance = __left0__ [0];
	var sorted_tuple = __left0__ [1];
	return tuple ([sorted_distance, sorted_tuple]);
};
var insertionSort = function (alist, main_list) {
	for (var index = 1; index < len (alist); index++) {
		var currentvalue = alist [index];
		var currentvalue_ml = main_list [index];
		var position = index;
		while (position > 0 && alist [position - 1] > currentvalue) {
			alist [position] = alist [position - 1];
			main_list [position] = main_list [position - 1];
			var position = position - 1;
		}
		alist [position] = currentvalue;
		main_list [position] = currentvalue_ml;
	}
	return tuple ([alist, main_list]);
};
var convert_to_decimal = function (binary_str) {
	var binary_str = '0b' + binary_str;
	return int (binary_str, 2);
};
var convert_to_binary = function (dec) {
	var ary = (function () {
		var __accu0__ = [];
		for (var i = 0; i < 16; i++) {
			__accu0__.append ('0');
		}
		return __accu0__;
	}) ();
	var itr = 15;
	while (dec != 0) {
		var rem = __mod__ (dec, 2);
		ary [itr] = str (rem);
		itr--;
		var dec = Math.floor (dec / 2);
	}
	return ''.join (ary);
};
var fuel_less_check = function (robot) {
	if (robot.me.turn > 200 && robot.fuel < 2000) {
		return true;
	}
	else if (robot.me.unit != constants.unit_pilgrim && robot.fuel < 200) {
		return true;
	}
	else {
		return false;
	}
};

var __module_utility__ = /*#__PURE__*/Object.freeze({
    is_out_of_bounds: is_out_of_bounds,
    is_cell_occupied: is_cell_occupied,
    random_cells_around: random_cells_around,
    get_relative_karbonite_mine_positions: get_relative_karbonite_mine_positions,
    get_relative_fuel_mine_positions: get_relative_fuel_mine_positions,
    get_relative_mine_positions: get_relative_mine_positions,
    insertionSort: insertionSort,
    convert_to_decimal: convert_to_decimal,
    convert_to_binary: convert_to_binary,
    fuel_less_check: fuel_less_check
});

// Transcrypt'ed from Python, 2019-01-14 14:01:45
var constants$1 = {};
var math$1 = {};
var utility = {};
__nest__ (constants$1, '', __module_constants__);
__nest__ (utility, '', __module_utility__);
__nest__ (math$1, '', __module_math__);
var _is_higher_than = function (a, b) {
	if (a == null || b == null) {
		return true;
	}
	return a [1] > b [1] || a [1] == b [1] && a [2] < b [2];
};
var astar_search = function (robot, pos_initial, pos_final, unit_type_move) {
	if (typeof unit_type_move == 'undefined' || (unit_type_move != null && unit_type_move.hasOwnProperty ("__kwargtrans__"))) {		var unit_type_move = 2;
	}	if (unit_type_move == 2) {
		var dirs = [tuple ([0, 1]), tuple ([0, -(1)]), tuple ([1, 0]), tuple ([-(1), 0]), tuple ([-(1), 1]), tuple ([1, 1]), tuple ([1, -(1)]), tuple ([-(1), -(1)]), tuple ([0, 2]), tuple ([0, -(2)]), tuple ([2, 0]), tuple ([-(2), 0])];
	}
	else if (unit_type_move == 1) {
		var dirs = [tuple ([0, 1]), tuple ([0, -(1)]), tuple ([1, 0]), tuple ([-(1), 0]), tuple ([-(1), 1]), tuple ([1, 1]), tuple ([1, -(1)]), tuple ([-(1), -(1)])];
	}
	else if (unit_type_move == 3) {
		var dirs = [tuple ([0, 1]), tuple ([0, -(1)]), tuple ([1, 0]), tuple ([-(1), 0]), tuple ([-(1), 1]), tuple ([1, 1]), tuple ([1, -(1)]), tuple ([-(1), -(1)]), tuple ([0, 2]), tuple ([0, -(2)]), tuple ([2, 0]), tuple ([-(2), 0]), tuple ([-(1), 2]), tuple ([1, 2]), tuple ([1, -(2)]), tuple ([-(1), -(2)]), tuple ([2, -(1)]), tuple ([2, 1]), tuple ([-(2), 1]), tuple ([-(2), -(1)]), tuple ([2, 2]), tuple ([2, -(2)]), tuple ([-(2), 2]), tuple ([-(2), -(2)]), tuple ([0, 3]), tuple ([0, -(3)]), tuple ([3, 0]), tuple ([-(3), 0])];
	}
	var nodes = [null];
	var insert_counter = 0;
	var block_kicker = 0;
	var came_from = dict ({});
	var cost_so_far = dict ({});
	came_from [pos_initial] = null;
	cost_so_far [pos_initial] = 0;
	var occupied_map = robot.get_visible_robot_map ();
	var passable_map = robot.get_passable_map ();
	if (utility.is_out_of_bounds (occupied_map, pos_final [0], pos_final [1]) || !(passable_map [pos_final [1]] [pos_final [0]])) {
		return null;
	}
	var retrace_path = function (pos_initial, pos_final, came_from) {
		var current = pos_final;
		var path = [];
		while (current != pos_initial) {
			path.append (current);
			var current = came_from [current];
		}
		path.reverse ();
		return path;
	};
	var neighbours = function (pos_intermediate) {
		var __left0__ = pos_intermediate;
		var pos_x = __left0__ [0];
		var pos_y = __left0__ [1];
		var result = [];
		for (var dirc of dirs) {
			var new_pos_x = pos_x + dirc [1];
			var new_pos_y = pos_y + dirc [0];
			if (!(utility.is_cell_occupied (occupied_map, new_pos_x, new_pos_y)) && passable_map [new_pos_y] [new_pos_x]) {
				result.append (tuple ([new_pos_x, new_pos_y]));
			}
		}
		return result;
	};
	var _heapify = function (nodes, new_node_index) {
		while (1 < new_node_index) {
			var new_node = nodes [new_node_index];
			if (__mod__ (new_node_index, 2) == 0) {
				var parent_index = new_node_index / 2;
			}
			else {
				var parent_index = (new_node_index - 1) / 2;
			}
			var parent_node = nodes [parent_index];
			if (_is_higher_than (parent_node, new_node)) {
				break;
			}
			var tmp_node = parent_node;
			nodes [parent_index] = new_node;
			nodes [new_node_index] = tmp_node;
			var new_node_index = parent_index;
		}
		return nodes;
	};
	var add = function (nodes, value, priority, insert_counter) {
		var new_node_index = len (nodes);
		insert_counter++;
		nodes.append (tuple ([value, priority, insert_counter]));
		_heapify (nodes, new_node_index);
		return insert_counter;
	};
	var py_pop = function (nodes) {
		if (len (nodes) == 1) {
			var __except0__ = LookupError ('Heap is empty');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		var result = nodes [1] [0];
		var empty_space_index = 1;
		while (empty_space_index * 2 < len (nodes)) {
			var left_child_index = empty_space_index * 2;
			var right_child_index = empty_space_index * 2 + 1;
			if (len (nodes) <= right_child_index || _is_higher_than (nodes [left_child_index], nodes [right_child_index])) {
				nodes [empty_space_index] = nodes [left_child_index];
				var empty_space_index = left_child_index;
			}
			else {
				nodes [empty_space_index] = nodes [right_child_index];
				var empty_space_index = right_child_index;
			}
		}
		var last_node_index = len (nodes) - 1;
		nodes [empty_space_index] = nodes [last_node_index];
		_heapify (nodes, empty_space_index);
		nodes.py_pop ();
		return result;
	};
	var astar_heuristic = function (pos_intermediate, pos_final) {
		var __left0__ = pos_intermediate;
		var x1 = __left0__ [0];
		var y1 = __left0__ [1];
		var __left0__ = pos_final;
		var x2 = __left0__ [0];
		var y2 = __left0__ [1];
		var dx = abs (x1 - x2);
		var dy = abs (y1 - y2);
		var heuristic = dx + dy;
		return heuristic * constants$1.pathfinding_heuristic_multiplier;
	};
	var insert_counter = add (nodes, pos_initial, 0, insert_counter);
	while (len (nodes) > 1) {
		var current = py_pop (nodes);
		if (str (current) == str (pos_final) || block_kicker > 45) {
			return retrace_path (pos_initial, current, came_from);
		}
		for (var iter_a of neighbours (current)) {
			var new_cost = cost_so_far [current] + 1;
			if (len (iter_a) != 0 && (!__in__ (iter_a, cost_so_far) || new_cost < cost_so_far [iter_a])) {
				cost_so_far [iter_a] = new_cost;
				var priority = new_cost + astar_heuristic (iter_a, pos_final);
				var insert_counter = add (nodes, iter_a, -(priority), insert_counter);
				came_from [iter_a] = current;
			}
		}
		block_kicker++;
	}
	return retrace_path (pos_initial, pos_final, came_from);
};

var __module_pathfinding__ = /*#__PURE__*/Object.freeze({
    _is_higher_than: _is_higher_than,
    astar_search: astar_search
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var utility$1 = {};
__nest__ (utility$1, '', __module_utility__);
var sort_visible_units_by_distance = function (robot) {
	var visible = robot.get_visible_robots ();
	var bots = [];
	var bots_distance = [];
	if (visible == null) {
		return [];
	}
	for (var r of visible) {
		if (!(robot.is_visible (r))) {
			continue;
		}
		bots_distance.append (Math.pow (r ['x'] - robot.me ['x'], 2) + Math.pow (r ['y'] - robot.me ['y'], 2));
		bots.append (r);
	}
	var __left0__ = utility$1.insertionSort (bots_distance, bots);
	var sorted_distance = __left0__ [0];
	var sorted_tuple = __left0__ [1];
	return tuple ([sorted_distance, sorted_tuple]);
};
var sort_visible_friendlies_by_distance = function (robot) {
	var visible = robot.get_visible_robots ();
	var friendly_bots = [];
	var friendly_bots_distance = [];
	if (visible == null) {
		return [];
	}
	for (var r of visible) {
		if (!(robot.is_visible (r))) {
			continue;
		}
		if (r ['team'] == robot.me ['team']) {
			friendly_bots_distance.append (Math.pow (r ['x'] - robot.me ['x'], 2) + Math.pow (r ['y'] - robot.me ['y'], 2));
			friendly_bots.append (r);
		}
	}
	var __left0__ = utility$1.insertionSort (friendly_bots_distance, friendly_bots);
	var sorted_distance = __left0__ [0];
	var sorted_tuple = __left0__ [1];
	return tuple ([sorted_distance, sorted_tuple]);
};
var sort_visible_enemies_by_distance = function (robot) {
	var visible = robot.get_visible_robots ();
	var enemy_bots = [];
	var enemy_bots_distance = [];
	if (visible == null) {
		return [];
	}
	for (var r of visible) {
		if (!(robot.is_visible (r))) {
			continue;
		}
		if (r ['team'] != robot.me ['team']) {
			enemy_bots_distance.append (Math.pow (r ['x'] - robot.me ['x'], 2) + Math.pow (r ['y'] - robot.me ['y'], 2));
			enemy_bots.append (r);
		}
	}
	var __left0__ = utility$1.insertionSort (enemy_bots_distance, enemy_bots);
	var sorted_distance = __left0__ [0];
	var sorted_tuple = __left0__ [1];
	return tuple ([sorted_distance, sorted_tuple]);
};
var all_karbonite = function (robot) {
	var karb_count = 0;
	for (var row of robot.karbonite_map) {
		for (var cell of row) {
			if (cell == true) {
				karb_count++;
			}
		}
	}
	return karb_count;
};
var all_fuel = function (robot) {
	var fuel_count = 0;
	for (var row of robot.fuel_map) {
		for (var cell of row) {
			if (cell == true) {
				fuel_count++;
			}
		}
	}
	return fuel_count;
};

var __module_vision__ = /*#__PURE__*/Object.freeze({
    sort_visible_units_by_distance: sort_visible_units_by_distance,
    sort_visible_friendlies_by_distance: sort_visible_friendlies_by_distance,
    sort_visible_enemies_by_distance: sort_visible_enemies_by_distance,
    all_karbonite: all_karbonite,
    all_fuel: all_fuel
});

// Transcrypt'ed from Python, 2019-01-14 14:01:45
var constants$2 = {};
var pathfinding = {};
var vision = {};
__nest__ (pathfinding, '', __module_pathfinding__);
__nest__ (vision, '', __module_vision__);
__nest__ (constants$2, '', __module_constants__);
var give_military_command = function (robot, recieved_message, self_signal) {
	if (typeof recieved_message == 'undefined' || (recieved_message != null && recieved_message.hasOwnProperty ("__kwargtrans__"))) {		var recieved_message = 0;
	}	if (typeof self_signal == 'undefined' || (self_signal != null && self_signal.hasOwnProperty ("__kwargtrans__"))) {		var self_signal = 0;
	}	if (recieved_message == 0 && self_signal == 0) {
		return default_military_behaviour (robot);
	}
};
var _crusader_combat = function (robot) {
	var __left0__ = vision.sort_visible_enemies_by_distance (robot);
	var visible_enemy_distance = __left0__ [0];
	var visible_enemy_list = __left0__ [1];
	if (len (visible_enemy_list) == 0) {
		return null;
	}
	else {
		var unit_attackrange_max = constants$2.crusader_max_attack_range;
		var unit_current_pos = tuple ([robot.me.x, robot.me.y]);
		var unit_will_attack_list = [];
		var unit_will_attack_pilgrim_list = [];
		for (var iter_i = 0; iter_i < len (visible_enemy_list); iter_i++) {
			var enemy = visible_enemy_list [iter_i];
			var enemy_distance = visible_enemy_distance [iter_i];
			if (enemy_distance <= unit_attackrange_max) {
				if (enemy ['unit'] == constants$2.unit_pilgrim) {
					unit_will_attack_pilgrim_list.append (enemy);
				}
				else {
					unit_will_attack_list.append (enemy);
				}
			}
		}
		if (len (unit_will_attack_list) != 0) {
			var enemy = unit_will_attack_list [0];
			return robot.attack (enemy ['x'] - unit_current_pos [0], enemy ['y'] - unit_current_pos [1]);
		}
		else if (len (unit_will_attack_pilgrim_list) != 0) {
			var enemy = unit_will_attack_pilgrim_list [0];
			return robot.attack (enemy ['x'] - unit_current_pos [0], enemy ['y'] - unit_current_pos [1]);
		}
		else {
			var enemy = visible_enemy_list [0];
			var move_to = pathfinding.astar_search (robot, unit_current_pos, tuple ([enemy ['x'], enemy ['y']]), 3) [0];
			if (move_to != null && len (move_to) != 0) {
				var __left0__ = move_to;
				var new_pos_x = __left0__ [0];
				var new_pos_y = __left0__ [1];
				return robot.move (new_pos_x - unit_current_pos [0], new_pos_y - unit_current_pos [1]);
			}
		}
		return null;
	}
};
var _prophet_combat = function (robot) {
	var __left0__ = vision.sort_visible_enemies_by_distance (robot);
	var visible_enemy_distance = __left0__ [0];
	var visible_enemy_list = __left0__ [1];
	if (len (visible_enemy_list) == 0) {
		return null;
	}
	else {
		var unit_attack_range_max = constants$2.prophet_max_attack_range;
		var unit_attack_range_min = constants$2.prophet_min_attack_range;
		var unit_current_pos = tuple ([robot.me.x, robot.me.y]);
		var unit_will_attack_list = [];
		var unit_will_attack_pilgrim_list = [];
		var unit_will_attack_id = [];
		for (var i = 0; i < len (visible_enemy_list); i++) {
			var enemy = visible_enemy_list [i];
			var enemy_distance = visible_enemy_distance [i];
			if (enemy_distance <= unit_attack_range_max && enemy_distance >= unit_attack_range_min) {
				if (!__in__ (enemy ['id'], robot.has_enemy_target_dict)) {
					robot.has_enemy_target_dict [enemy ['id']] = enemy;
				}
				if (enemy ['unit'] == constants$2.unit_pilgrim) {
					unit_will_attack_pilgrim_list.append (enemy);
				}
				else {
					unit_will_attack_list.append (enemy);
				}
				unit_will_attack_id.append (enemy ['id']);
			}
		}
		var target_robot_id = robot.is_targeting_robot_with_id;
		var enemy = null;
		if (len (unit_will_attack_list) != 0) {
			var enemy = unit_will_attack_list [0];
			robot.is_targeting_robot_with_id = enemy ['id'];
		}
		else if (len (unit_will_attack_pilgrim_list) != 0) {
			var enemy = unit_will_attack_pilgrim_list [0];
			robot.is_targeting_robot_with_id = enemy ['id'];
		}
		if (__in__ (target_robot_id, unit_will_attack_id)) {
			var old_enemy = robot.has_enemy_target_dict [target_robot_id];
			return robot.attack (old_enemy ['x'] - unit_current_pos [0], old_enemy ['y'] - unit_current_pos [1]);
		}
		if (enemy) {
			robot.is_targeting_robot_with_id = enemy ['id'];
			return robot.attack (enemy ['x'] - unit_current_pos [0], enemy ['y'] - unit_current_pos [1]);
		}
		return null;
	}
};
var _preacher_attack = function (robot) {
	var visible_friendly_list = [];
	var __left0__ = vision.sort_visible_enemies_by_distance (robot);
	var visible_enemy_distance = __left0__ [0];
	var visible_enemy_list = __left0__ [1];
	if (false) {
		var __left0__;
		var visible_friendly_distance;
		var visible_friendly_list;
	}
	if (len (visible_enemy_list) == 0) {
		return null;
	}
	else {
		var unit_attack_range_max = constants$2.preacher_max_attack_range;
		var unit_attack_range_min = constants$2.preacher_min_attack_range;
		var unit_current_pos = tuple ([robot.me.x, robot.me.y]);
		var unit_will_attack_list = [];
		var unit_will_attack_pilgrim_list = [];
		var friendly_list = [];
		for (var i = 0; i < len (visible_enemy_list); i++) {
			var enemy = visible_enemy_list [i];
			var enemy_distance = visible_enemy_distance [i];
			if (enemy_distance <= unit_attack_range_max && enemy_distance >= unit_attack_range_min) {
				if (enemy ['unit'] == constants$2.unit_pilgrim) {
					unit_will_attack_pilgrim_list.append (enemy);
				}
				else {
					unit_will_attack_list.append (enemy);
				}
			}
		}
		for (var i = 0; i < len (visible_friendly_list); i++) {
			var friendly = visible_friendly_list [i];
			var friendly_distance = visible_friendly_distance [i];
			if (friendly_distance <= unit_attack_range_max && friendly_distance >= unit_attack_range_min) {
				friendly_list.append (friendly);
			}
		}
		if (len (friendly_list) != 0) {
			if (false) {
				if (true) {
					var enemy;
				}
				else {
					var enemy;
				}
			}
		}
		else if (len (unit_will_attack_list) != 0) {
			var enemy = unit_will_attack_list [0];
			return robot.attack (enemy ['x'] - unit_current_pos [0], enemy ['y'] - unit_current_pos [1]);
		}
		else if (len (unit_will_attack_pilgrim_list) != 0) {
			var enemy = unit_will_attack_pilgrim_list [0];
			return robot.attack (enemy ['x'] - unit_current_pos [0], enemy ['y'] - unit_current_pos [1]);
		}
		return null;
	}
};
var default_military_behaviour = function (robot) {
	var unit_type = robot.me.unit;
	if (unit_type == constants$2.unit_crusader) {
		return _crusader_combat (robot);
	}
	else if (unit_type == constants$2.unit_preacher) {
		return _preacher_attack (robot);
	}
	else if (unit_type == constants$2.unit_prophet) {
		return _prophet_combat (robot);
	}
};
var pilgrimpriority = function () {
	return false;
};
var friendlyfire = function () {
	return false;
};

var __module_combat_module__ = /*#__PURE__*/Object.freeze({
    give_military_command: give_military_command,
    _crusader_combat: _crusader_combat,
    _prophet_combat: _prophet_combat,
    _preacher_attack: _preacher_attack,
    default_military_behaviour: default_military_behaviour,
    pilgrimpriority: pilgrimpriority,
    friendlyfire: friendlyfire
});

// Transcrypt'ed from Python, 2019-01-14 14:01:45
var combat_module = {};
var utility$2 = {};
__nest__ (combat_module, '', __module_combat_module__);
__nest__ (utility$2, '', __module_utility__);
var prophet = function (robot) {
	return prophet_move (robot);
};
var prophet_move = function (robot) {
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var passable_map = robot.get_passable_map ();
	var occupied_map = robot.get_visible_robot_map ();
	var directions = utility$2.random_cells_around ();
	var prophet_attack_aggr_mode = combat_module.give_military_command (robot);
	if (prophet_attack_aggr_mode != null) {
		return prophet_attack_aggr_mode;
	}
	if (utility$2.fuel_less_check (robot)) {
		return null;
	}
	for (var direction of directions) {
		if (!(utility$2.is_cell_occupied (occupied_map, pos_x + direction [1], pos_y + direction [0])) && passable_map [pos_y + direction [0]] [pos_x + direction [1]] == 1) {
			return robot.move (direction [1], direction [0]);
		}
	}
};

var __module_prophets__ = /*#__PURE__*/Object.freeze({
    prophet: prophet,
    prophet_move: prophet_move
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var combat_module$1 = {};
var utility$3 = {};
__nest__ (combat_module$1, '', __module_combat_module__);
__nest__ (utility$3, '', __module_utility__);
var preacher = function (robot) {
	return preacher_move (robot);
};
var preacher_move = function (robot) {
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var passable_map = robot.get_passable_map ();
	var occupied_map = robot.get_visible_robot_map ();
	var directions = utility$3.random_cells_around ();
	var preacher_attack_aggr_mode = combat_module$1.give_military_command (robot);
	if (preacher_attack_aggr_mode != null) {
		return preacher_attack_aggr_mode;
	}
	if (utility$3.fuel_less_check (robot)) {
		return null;
	}
	for (var direction of directions) {
		if (!(utility$3.is_cell_occupied (occupied_map, pos_x + direction [1], pos_y + direction [0])) && passable_map [pos_y + direction [0]] [pos_x + direction [1]] == 1) {
			return robot.move (direction [1], direction [0]);
		}
	}
};

var __module_preachers__ = /*#__PURE__*/Object.freeze({
    preacher: preacher,
    preacher_move: preacher_move
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var utility$4 = {};
__nest__ (utility$4, '', __module_utility__);
var message_to_castles = function (robot, mesg_type) {
	robot.castleTalk (mesg_type);
};
var self_communicate_loop = function (robot) {
	robot.signal (robot.me.signal, 0);
};
var convert_position_to_message = function (pos_x, pos_y) {
	return (pos_x * 100 + pos_y) + 6464;
};
var convert_message_to_position = function (message) {
	var message = message - 6464;
	return tuple ([Math.floor (message / 100), __mod__ (message, 100)]);
};
var can_compute_others = function (message) {
	var bin_str = utility$4.convert_to_binary (message);
	if (bin_str [0] == '0') {
		return false;
	}
	else {
		return true;
	}
};
var message_parsing = function (message, flag) {
	if (flag == 1) {
		return can_compute_others (message);
	}
	else {
		return false;
	}
};
var _store_destination = function (dest_x, dest_y, bin_list) {
	var x_bin = utility$4.convert_to_binary (dest_x);
	var y_bin = utility$4.convert_to_binary (dest_y);
	var start = 4;
	for (var i = 10; i < 16; i++) {
		bin_list [start] = x_bin [i];
		start++;
	}
	for (var i = 10; i < 16; i++) {
		bin_list [start] = y_bin [i];
		start++;
	}
};
var _store_next_step = function (astar_path, bin_list, directions) {
	if (len (astar_path) == 1) {
		bin_list [3] = '1';
		for (var i = 0; i < 3; i++) {
			bin_list [i] = '0';
		}
		return null;
	}
	var step = astar_path [0];
	var second_step = astar_path [1];
	var dx = second_step [0] - step [0];
	var dy = second_step [1] - step [1];
	var ans = null;
	for (var i = 0; i < len (directions); i++) {
		var direction = directions [i];
		if (tuple ([dx, dy]) == direction) {
			var ans = i;
			break;
		}
	}
	var step_byte = utility$4.convert_to_binary (ans);
	var iter_ = 0;
	for (var i = 12; i < 16; i++) {
		bin_list [iter_] = step_byte [i];
		iter_++;
	}
};
var encode_msg_with_direction = function (dest_x, dest_y, astar_path, directions) {
	var bin_list = (function () {
		var __accu0__ = [];
		for (var i = 0; i < 16; i++) {
			__accu0__.append ('0');
		}
		return __accu0__;
	}) ();
	_store_destination (dest_x, dest_y, bin_list);
	_store_next_step (astar_path, bin_list, directions);
	return utility$4.convert_to_decimal (''.join (bin_list));
};
var encode_msg_without_direction = function (dest_x, dest_y) {
	var bin_list = (function () {
		var __accu0__ = [];
		for (var i = 0; i < 16; i++) {
			__accu0__.append ('0');
		}
		return __accu0__;
	}) ();
	_store_destination (dest_x, dest_y, bin_list);
	return utility$4.convert_to_decimal (''.join (bin_list));
};
var decode_msg_with_direction = function (message, directions) {
	var binary_str = utility$4.convert_to_binary (message);
	var direction = utility$4.convert_to_decimal (binary_str.__getslice__ (0, 4, 1));
	var x_destination = utility$4.convert_to_decimal (binary_str.__getslice__ (4, 10, 1));
	var y_destination = utility$4.convert_to_decimal (binary_str.__getslice__ (10, 16, 1));
	return tuple ([direction, x_destination, y_destination]);
};
var decode_msg_without_direction = function (message) {
	var binary_str = utility$4.convert_to_binary (message);
	var x_destination = utility$4.convert_to_decimal (binary_str.__getslice__ (4, 10, 1));
	var y_destination = utility$4.convert_to_decimal (binary_str.__getslice__ (10, 16, 1));
	return tuple ([x_destination, y_destination]);
};

var __module_communications__ = /*#__PURE__*/Object.freeze({
    message_to_castles: message_to_castles,
    self_communicate_loop: self_communicate_loop,
    convert_position_to_message: convert_position_to_message,
    convert_message_to_position: convert_message_to_position,
    can_compute_others: can_compute_others,
    message_parsing: message_parsing,
    _store_destination: _store_destination,
    _store_next_step: _store_next_step,
    encode_msg_with_direction: encode_msg_with_direction,
    encode_msg_without_direction: encode_msg_without_direction,
    decode_msg_with_direction: decode_msg_with_direction,
    decode_msg_without_direction: decode_msg_without_direction
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var communications = {};
var constants$3 = {};
var pathfinding$1 = {};
var utility$5 = {};
__nest__ (utility$5, '', __module_utility__);
__nest__ (constants$3, '', __module_constants__);
__nest__ (pathfinding$1, '', __module_pathfinding__);
__nest__ (communications, '', __module_communications__);
var calculate_dir = function (start, target) {
	var dx = target [0] - start [0];
	var dy = target [1] - start [1];
	if (dx < 0) {
		var dx = -(1);
	}
	else if (dx > 0) {
		var dx = 1;
	}
	if (dy < 0) {
		var dy = -(1);
	}
	else if (dy > 0) {
		var dy = 1;
	}
	return tuple ([dx, dy]);
};
var is_completely_surrounded = function (robot) {
	var passable_map = robot.get_passable_map ();
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var occupied_map = robot.get_visible_robot_map ();
	if (robot.me.unit == constants$3.unit_crusader) {
		for (var direction of constants$3.crusader_move_directions) {
			if (!(utility$5.is_cell_occupied (occupied_map, pos_x + direction [1], pos_y + direction [0])) && passable_map [pos_y + direction [0]] [pos_x + direction [1]] == 1) {
				return false;
			}
		}
	}
	else {
		for (var direction of constants$3.non_crusader_move_directions) {
			if (!(utility$5.is_cell_occupied (occupied_map, pos_x + direction [1], pos_y + direction [0])) && passable_map [pos_y + direction [0]] [pos_x + direction [1]] == 1) {
				return false;
			}
		}
	}
	return true;
};

var __module_movement__ = /*#__PURE__*/Object.freeze({
    calculate_dir: calculate_dir,
    is_completely_surrounded: is_completely_surrounded
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var communications$1 = {};
var constants$4 = {};
var movement = {};
var pathfinding$2 = {};
var utility$6 = {};
var vision$1 = {};
__nest__ (movement, '', __module_movement__);
__nest__ (pathfinding$2, '', __module_pathfinding__);
__nest__ (constants$4, '', __module_constants__);
__nest__ (communications$1, '', __module_communications__);
__nest__ (vision$1, '', __module_vision__);
__nest__ (utility$6, '', __module_utility__);
var pilgrim = function (robot) {
	var carry_karb = robot.me.karbonite;
	var carry_fuel = robot.me.fuel;
	if (carry_fuel > 80 || carry_karb > 18) {
		return pilgrim_full (robot);
	}
	var pilgrim_is_mining = pilgrim_mine (robot);
	if (pilgrim_is_mining != 0) {
		return pilgrim_is_mining;
	}
	if (robot.me.signal == 0 && robot.current_move_destination == null) {
		var __left0__ = vision$1.sort_visible_friendlies_by_distance (robot);
		var unused_store = __left0__ [0];
		var friendly_units = __left0__ [1];
		for (var friendly_unit of friendly_units) {
			if (friendly_unit.unit == 0 && friendly_unit.signal > 0) {
				_pilgrims_initial_check (robot, friendly_unit);
				break;
			}
		}
	}
	if (utility$6.fuel_less_check (robot)) {
		return null;
	}
	var pilgrim_is_moving = pilgrim_move (robot);
	if (pilgrim_is_moving != 0) {
		return pilgrim_is_moving;
	}
};
var _pilgrims_initial_check = function (robot, friendly_unit) {
	robot.built_by_a_castle = 1;
	robot.current_move_destination = communications$1.decode_msg_without_direction (friendly_unit.signal);
	robot.our_castle_or_church_base = tuple ([friendly_unit ['x'], friendly_unit ['y']]);
	robot.our_original_castle_location = robot.our_castle_or_church_base;
	robot.pilgrim_mine_ownership = 1;
};
var pilgrim_move = function (robot) {
	if (robot.fuel <= 2) {
		return 0;
	}
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var passable_map = robot.get_passable_map ();
	var karb_map = robot.get_karbonite_map ();
	var fuel_map = robot.get_fuel_map ();
	var occupied_map = robot.get_visible_robot_map ();
	var random_directions = utility$6.random_cells_around ();
	if (movement.is_completely_surrounded (robot)) {
		robot.log ('Completely surrounded pilgrim');
		return 0;
	}
	if (robot.me.turn > constants$4.pilgrim_will_scavenge_closeby_mines_after_turns && robot.me.turn < constants$4.pilgrim_will_scavenge_closeby_mines_before_turns) {
		for (var direction of random_directions) {
			if (!(utility$6.is_cell_occupied (occupied_map, pos_x + direction [1], pos_y + direction [0])) && (karb_map [pos_y + direction [0]] [pos_x + direction [1]] == 1 || fuel_map [pos_y + direction [0]] [pos_x + direction [1]] == 1)) {
				return robot.move (direction [1], direction [0]);
			}
		}
	}
	if (robot.current_move_destination != null) {
		var final_pos_x = robot.current_move_destination [0];
		var final_pos_y = robot.current_move_destination [1];
		if (utility$6.is_cell_occupied (occupied_map, final_pos_x, final_pos_y)) {
			if (robot.pilgrim_type != 2) {
				robot.pilgrim_type = 2;
				var __left0__ = utility$6.get_relative_mine_positions (robot);
				var unused_store = __left0__ [0];
				robot.pilgrim_scavenge_mine_location_list = __left0__ [1];
				robot.pilgrim_scavenge_mine_occupancy_list = (function () {
					var __accu0__ = [];
					for (var i = 0; i < len (robot.pilgrim_scavenge_mine_location_list); i++) {
						__accu0__.append (-(1));
					}
					return __accu0__;
				}) ();
			}
			for (var iter_i = 0; iter_i < len (robot.pilgrim_scavenge_mine_location_list); iter_i++) {
				if (robot.pilgrim_scavenge_mine_occupancy_list [iter_i] == -(1)) {
					robot.pilgrim_scavenge_mine_occupancy_list [iter_i] = 0;
					if (str (robot.current_move_destination) != str (robot.pilgrim_scavenge_mine_location_list [iter_i])) {
						robot.current_move_destination = robot.pilgrim_scavenge_mine_location_list [iter_i];
						robot.mov_path_between_base_and_mine = null;
						break;
					}
				}
			}
		}
	}
	if (robot.current_move_destination != null) {
		if (robot.mov_path_between_base_and_mine == null || robot.has_made_random_movement != 0) {
			robot.has_made_random_movement = 0;
			robot.mov_path_between_base_and_mine = pathfinding$2.astar_search (robot, tuple ([robot.me.x, robot.me.y]), robot.current_move_destination, 2);
			if (robot.mov_path_between_base_and_mine != null) {
				robot.mov_path_index = 0;
				var __left0__ = robot.mov_path_between_base_and_mine [robot.mov_path_index];
				var new_pos_x = __left0__ [0];
				var new_pos_y = __left0__ [1];
				return robot.move (new_pos_x - pos_x, new_pos_y - pos_y);
			}
		}
		else if (len (robot.mov_path_between_base_and_mine) - 1 == robot.mov_path_index + 1) {
			robot.mov_path_index = robot.mov_path_index + 1;
			if (str (robot.mov_path_between_base_and_mine [robot.mov_path_index]) == str (robot.current_move_destination)) {
				var __left0__ = robot.mov_path_between_base_and_mine [robot.mov_path_index];
				var new_pos_x = __left0__ [0];
				var new_pos_y = __left0__ [1];
				if (!(utility$6.is_cell_occupied (occupied_map, new_pos_x, new_pos_y))) {
					robot.pilgrim_mine_ownership = robot.current_move_destination;
					robot.current_move_destination = null;
					robot.mov_path_index = 0;
					return robot.move (new_pos_x - pos_x, new_pos_y - pos_y);
				}
			}
			else {
				robot.mov_path_between_base_and_mine = pathfinding$2.astar_search (robot, tuple ([robot.me.x, robot.me.y]), robot.current_move_destination, 2);
				robot.mov_path_index = 0;
				var __left0__ = robot.mov_path_between_base_and_mine [robot.mov_path_index];
				var new_pos_x = __left0__ [0];
				var new_pos_y = __left0__ [1];
				return robot.move (new_pos_x - pos_x, new_pos_y - pos_y);
			}
		}
		else {
			robot.mov_path_index = robot.mov_path_index + 1;
			var __left0__ = robot.mov_path_between_base_and_mine [robot.mov_path_index];
			var new_pos_x = __left0__ [0];
			var new_pos_y = __left0__ [1];
			if (utility$6.is_cell_occupied (occupied_map, new_pos_x, new_pos_y)) {
				robot.mov_path_between_base_and_mine = pathfinding$2.astar_search (robot, tuple ([robot.me.x, robot.me.y]), robot.current_move_destination, 2);
				robot.mov_path_index = 0;
				var __left0__ = robot.mov_path_between_base_and_mine [robot.mov_path_index];
				var new_pos_x = __left0__ [0];
				var new_pos_y = __left0__ [1];
			}
			return robot.move (new_pos_x - pos_x, new_pos_y - pos_y);
		}
	}
	for (var direction of random_directions) {
		if (!(utility$6.is_cell_occupied (occupied_map, pos_x + direction [1], pos_y + direction [0])) && passable_map [pos_y + direction [0]] [pos_x + direction [1]] == 1) {
			robot.has_made_random_movement = 1;
			return robot.move (direction [1], direction [0]);
		}
	}
	return 0;
};
var pilgrim_mine = function (robot) {
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var karb_map = robot.get_karbonite_map ();
	var fuel_map = robot.get_fuel_map ();
	if (karb_map [pos_y] [pos_x] == 1 || fuel_map [pos_y] [pos_x] == 1) {
		robot.signal (0, 0);
		return robot.mine ();
	}
	else {
		return 0;
	}
};
var pilgrim_full = function (robot) {
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var carry_karb = robot.me.karbonite;
	var carry_fuel = robot.me.fuel;
	var karb_map = robot.get_karbonite_map ();
	var fuel_map = robot.get_fuel_map ();
	var passable_map = robot.get_passable_map ();
	var occupied_map = robot.get_visible_robot_map ();
	var directions$$1 = constants$4.directions;
	if (karb_map [pos_y] [pos_x] == 1 || fuel_map [pos_y] [pos_x] == 1) {
		var __left0__ = vision$1.sort_visible_friendlies_by_distance (robot);
		var unused_store = __left0__ [0];
		var friendly_units = __left0__ [1];
		if (friendly_units != null || len (friendly_units) != 0) {
			for (var f_unit of friendly_units) {
				var dx = f_unit.x - pos_x;
				var dy = f_unit.y - pos_y;
				if (f_unit.unit == constants$4.unit_church || f_unit.unit == constants$4.unit_castle) {
					for (var direction of directions$$1) {
						if (direction [1] == dx && direction [0] == dy) {
							robot.signal (0, 0);
							return robot.give (dx, dy, carry_karb, carry_fuel);
						}
					}
				}
			}
		}
	}
	if (robot.karbonite > 50 && robot.fuel > 200) {
		return _make_church (robot);
	}
};
var _make_church = function (robot) {
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var karb_map = robot.get_karbonite_map ();
	var fuel_map = robot.get_fuel_map ();
	var passable_map = robot.get_passable_map ();
	var occupied_map = robot.get_visible_robot_map ();
	var directions$$1 = constants$4.directions;
	var potential_church_postitons = [];
	for (var p_church_pos of directions$$1) {
		if (!(utility$6.is_cell_occupied (occupied_map, pos_x + p_church_pos [1], pos_y + p_church_pos [0])) && passable_map [pos_y + p_church_pos [0]] [pos_x + p_church_pos [1]] == 1 && karb_map [pos_y + p_church_pos [0]] [pos_x + p_church_pos [1]] != 1 && fuel_map [pos_y + p_church_pos [0]] [pos_x + p_church_pos [1]] != 1) {
			var count = 0;
			for (var direction of directions$$1) {
				if (!(utility$6.is_out_of_bounds (len (occupied_map), (pos_x + p_church_pos [1]) + direction [1], (pos_y + p_church_pos [0]) + direction [0]))) {
					if (karb_map [(pos_y + p_church_pos [0]) + direction [0]] [(pos_x + p_church_pos [1]) + direction [1]] == 1 || fuel_map [(pos_y + p_church_pos [0]) + direction [0]] [(pos_x + p_church_pos [1]) + direction [1]] == 1) {
						count++;
					}
				}
			}
			potential_church_postitons.append (tuple ([p_church_pos [0], p_church_pos [1], count]));
		}
	}
	var max_resource_pos = tuple ([0, 0, 0]);
	for (var pos of potential_church_postitons) {
		if (pos [2] > max_resource_pos [2]) {
			var max_resource_pos = pos;
		}
	}
	robot.log (((('Making a church at (' + int (pos_x + max_resource_pos [1])) + ', ') + int (pos_y + max_resource_pos [0])) + ')');
	robot.signal (0, 0);
	return robot.build_unit (constants$4.unit_church, max_resource_pos [1], max_resource_pos [0]);
};

var __module_pilgrims__ = /*#__PURE__*/Object.freeze({
    pilgrim: pilgrim,
    _pilgrims_initial_check: _pilgrims_initial_check,
    pilgrim_move: pilgrim_move,
    pilgrim_mine: pilgrim_mine,
    pilgrim_full: pilgrim_full,
    _make_church: _make_church
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var combat_module$2 = {};
var utility$7 = {};
__nest__ (combat_module$2, '', __module_combat_module__);
__nest__ (utility$7, '', __module_utility__);
var crusader = function (robot) {
	return crusader_move (robot);
};
var crusader_move = function (robot) {
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var passable_map = robot.get_passable_map ();
	var occupied_map = robot.get_visible_robot_map ();
	var directions = utility$7.random_cells_around ();
	var crusader_is_attacking_or_aggressive_moving = combat_module$2.give_military_command (robot);
	if (crusader_is_attacking_or_aggressive_moving != null) {
		return crusader_is_attacking_or_aggressive_moving;
	}
	for (var direction of directions) {
		if (!(utility$7.is_cell_occupied (occupied_map, pos_x + direction [1], pos_y + direction [0])) && passable_map [pos_y + direction [0]] [pos_x + direction [1]] == 1) {
			return robot.move (direction [1], direction [0]);
		}
	}
};

var __module_crusaders__ = /*#__PURE__*/Object.freeze({
    crusader: crusader,
    crusader_move: crusader_move
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var constants$5 = {};
var utility$8 = {};
__nest__ (utility$8, '', __module_utility__);
__nest__ (constants$5, '', __module_constants__);
var _build_manager_castle = function (robot) {
};
var _build_manager_church = function (robot) {
	var unit_type = constants$5.unit_prophet;
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var occupied_map = robot.get_visible_robot_map ();
	var passable_map = robot.get_passable_map ();
	var directions$$1 = utility$8.random_cells_around ();
	for (var direction of directions$$1) {
		if (!(utility$8.is_cell_occupied (occupied_map, pos_x + direction [1], pos_y + direction [0])) && passable_map [pos_y + direction [0]] [pos_x + direction [1]] == 1) {
			return robot.build_unit (unit_type, direction [1], direction [0]);
		}
	}
	robot.log ('No space to build units anymore for churches');
	return null;
};
var default_production_order = function (robot) {
	var unit_type = robot.me.unit;
	if (unit_type == constants$5.unit_church) {
		return _build_manager_church (robot);
	}
	if (unit_type == constants$5.unit_castle) {
		return _build_manager_castle (robot);
	}
};

var __module_production_module__ = /*#__PURE__*/Object.freeze({
    _build_manager_castle: _build_manager_castle,
    _build_manager_church: _build_manager_church,
    default_production_order: default_production_order
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var constants$6 = {};
var production_module = {};
var utility$9 = {};
__nest__ (production_module, '', __module_production_module__);
__nest__ (constants$6, '', __module_constants__);
__nest__ (utility$9, '', __module_utility__);
var church = function (robot) {
	if (robot.step < 2) {
		return production_module.default_production_order (robot);
	}
};

var __module_churches__ = /*#__PURE__*/Object.freeze({
    church: church
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var constants$7 = {};
__nest__ (constants$7, '', __module_constants__);
var get_nearby_map = function (x, y, given_map, grid_radius) {
	if (typeof grid_radius == 'undefined' || (grid_radius != null && grid_radius.hasOwnProperty ("__kwargtrans__"))) {		var grid_radius = 2;
	}	var sub_side = grid_radius * 2 + 1;
	var sub_map = [];
	for (var i = 0; i < sub_side; i++) {
		for (var j = 0; j < sub_side; j++) {
			try {
				sub_map.append (given_map [(y - grid_radius) + i] [(x - grid_radius) + j] == true);
			}
			catch (__except0__) {
				sub_map.append (false);
			}
		}
	}
	return sub_map;
};
var get_map_ratio = function (x, y, given_map, grid_radius) {
	if (typeof grid_radius == 'undefined' || (grid_radius != null && grid_radius.hasOwnProperty ("__kwargtrans__"))) {		var grid_radius = 2;
	}	var nearby = get_nearby_map (x, y, given_map, grid_radius);
	var full = 0;
	for (var cell of nearby) {
		if (cell == true) {
			full++;
		}
	}
	return full / Math.pow (grid_radius * 2 + 1, 2);
};
var analyze_map = function (given_map, grid_radius) {
	if (typeof grid_radius == 'undefined' || (grid_radius != null && grid_radius.hasOwnProperty ("__kwargtrans__"))) {		var grid_radius = 2;
	}	var sub_side = grid_radius * 2 + 1;
	var results = [];
	var y = grid_radius + 1;
	while (y < len (given_map)) {
		var x = grid_radius + 1;
		while (x < len (given_map)) {
			results.append (tuple ([x, y, get_map_ratio (x, y, given_map, grid_radius)]));
			x += sub_side;
		}
		y += sub_side;
	}
	return results;
};
var check_hoz_symmetry = function (given_map) {
	var start = 0;
	var end = len (given_map) - 1;
	while (start < end) {
		for (var i = 0; i < len (given_map [start]); i++) {
			if (given_map [start] [i] != given_map [end] [i]) {
				return false;
			}
		}
		start++;
		end--;
	}
	return true;
};
var find_chokepoints = function (robot, grid_radius) {
	if (typeof grid_radius == 'undefined' || (grid_radius != null && grid_radius.hasOwnProperty ("__kwargtrans__"))) {		var grid_radius = 2;
	}	var given_map = robot.get_passable_map ();
	var sub_side = grid_radius * 2 + 1;
	var results = [];
	var y = grid_radius + 1;
	while (y < len (given_map)) {
		var x = grid_radius + 1;
		while (x < len (given_map)) {
			var ratio = get_map_ratio (x, y, given_map, grid_radius);
			if (ratio < constants$7.chokepoint_modifier) {
				results.append (tuple ([x, y, ratio]));
			}
			x += sub_side;
		}
		y += sub_side;
	}
	return results;
};
var find_karbonite_rich = function (robot, grid_radius) {
	if (typeof grid_radius == 'undefined' || (grid_radius != null && grid_radius.hasOwnProperty ("__kwargtrans__"))) {		var grid_radius = 2;
	}	var given_map = robot.karbonite_map;
	var sub_side = grid_radius * 2 + 1;
	var results = [];
	var y = grid_radius + 1;
	while (y < len (given_map)) {
		var x = grid_radius + 1;
		while (x < len (given_map)) {
			var ratio = get_map_ratio (x, y, given_map, grid_radius);
			if (ratio > constants$7.karbonite_modifier) {
				results.append (tuple ([x, y, ratio]));
			}
			x += sub_side;
		}
		y += sub_side;
	}
	return results;
};
var find_fuel_rich = function (robot, grid_radius) {
	if (typeof grid_radius == 'undefined' || (grid_radius != null && grid_radius.hasOwnProperty ("__kwargtrans__"))) {		var grid_radius = 2;
	}	var given_map = robot.fuel_map;
	var sub_side = grid_radius * 2 + 1;
	var results = [];
	var y = grid_radius + 1;
	while (y < len (given_map)) {
		var x = grid_radius + 1;
		while (x < len (given_map)) {
			var ratio = get_map_ratio (x, y, given_map, grid_radius);
			if (ratio > constants$7.fuel_modifier) {
				results.append (tuple ([x, y, ratio]));
			}
			x += sub_side;
		}
		y += sub_side;
	}
	return results;
};
var find_resource_rich = function (robot, grid_radius) {
	if (typeof grid_radius == 'undefined' || (grid_radius != null && grid_radius.hasOwnProperty ("__kwargtrans__"))) {		var grid_radius = 2;
	}	var fuel_map = robot.fuel_map;
	var karbonite_map = robot.karbonite_map;
	var sub_side = grid_radius * 2 + 1;
	var results = [];
	var y = grid_radius + 1;
	while (y < len (fuel_map)) {
		var x = grid_radius + 1;
		while (x < len (fuel_map)) {
			var ratio = get_map_ratio (x, y, fuel_map, grid_radius) + get_map_ratio (x, y, karbonite_map, grid_radius);
			if (ratio > constants$7.fuel_modifier) {
				results.append (tuple ([x, y, ratio]));
			}
			x += sub_side;
		}
		y += sub_side;
	}
	return results;
};

var __module_mapping__ = /*#__PURE__*/Object.freeze({
    get_nearby_map: get_nearby_map,
    get_map_ratio: get_map_ratio,
    analyze_map: analyze_map,
    check_hoz_symmetry: check_hoz_symmetry,
    find_chokepoints: find_chokepoints,
    find_karbonite_rich: find_karbonite_rich,
    find_fuel_rich: find_fuel_rich,
    find_resource_rich: find_resource_rich
});

// Transcrypt'ed from Python, 2019-01-14 14:01:46
var communications$2 = {};
var constants$8 = {};
var mapping = {};
var utility$a = {};
var vision$2 = {};
__nest__ (constants$8, '', __module_constants__);
__nest__ (mapping, '', __module_mapping__);
__nest__ (vision$2, '', __module_vision__);
__nest__ (communications$2, '', __module_communications__);
__nest__ (utility$a, '', __module_utility__);
var castle = function (robot) {
	_castle_initial_check (robot);
	var pilgrim_count = 0;
	var prophet_count = 0;
	var friendly_units = castle_all_friendly_units (robot);
	var total_karbonite = vision$2.all_karbonite (robot);
	var total_fuel = vision$2.all_fuel (robot);
	for (var f_unit of friendly_units) {
		if (f_unit.castle_talk == constants$8.unit_castle) ;
		else if (f_unit.castle_talk == constants$8.unit_church) ;
		else if (f_unit.castle_talk == constants$8.unit_crusader) ;
		else if (f_unit.castle_talk == constants$8.unit_pilgrim) {
			pilgrim_count++;
		}
		else if (f_unit.castle_talk == constants$8.unit_preacher) ;
		else if (f_unit.castle_talk == constants$8.unit_prophet) {
			prophet_count++;
		}
	}
	if (robot.step < 2 && robot.karbonite > 60) {
		robot.pilgrim_build_number++;
		robot.signal (_castle_assign_mine_or_scout (robot), 2);
		return castle_build (robot, constants$8.unit_pilgrim);
	}
	else if (robot.karbonite > 100 && robot.fuel > 200) {
		if (prophet_count < pilgrim_count) {
			return castle_build (robot, constants$8.unit_prophet);
		}
		else if (pilgrim_count < (total_fuel + total_karbonite) * 0.55) {
			robot.pilgrim_build_number++;
			robot.signal (_castle_assign_mine_or_scout (robot), 2);
			return castle_build (robot, constants$8.unit_pilgrim);
		}
		else if (robot.step > 500 && robot.karbonite > 300 && robot.fuel > 300) {
			return castle_build (robot, constants$8.unit_prophet);
		}
	}
};
var _castle_initial_check = function (robot) {
	if (len (robot.fuel_mine_locations_from_this_castle) == 0) {
		var __left0__ = utility$a.get_relative_fuel_mine_positions (robot);
		var unused_store = __left0__ [0];
		robot.fuel_mine_locations_from_this_castle = __left0__ [1];
		robot.fuel_mine_occupancy_from_this_castle = (function () {
			var __accu0__ = [];
			for (var i = 0; i < len (robot.fuel_mine_locations_from_this_castle); i++) {
				__accu0__.append (-(1));
			}
			return __accu0__;
		}) ();
	}
	if (len (robot.karb_mine_locations_from_this_castle) == 0) {
		var __left0__ = utility$a.get_relative_karbonite_mine_positions (robot);
		var unused_store = __left0__ [0];
		robot.karb_mine_locations_from_this_castle = __left0__ [1];
		robot.karb_mine_occupancy_from_this_castle = (function () {
			var __accu0__ = [];
			for (var i = 0; i < len (robot.karb_mine_locations_from_this_castle); i++) {
				__accu0__.append (-(1));
			}
			return __accu0__;
		}) ();
	}
	if (robot.castle_health == null) {
		robot.castle_health = constants$8.castle_max_health;
	}
	else if (robot.me.health < robot.castle_health) {
		robot.castle_health = robot.me.health;
		robot.castle_under_attack = 1;
		robot.castle_under_attack_turn = robot.step;
	}
	else if (robot.castle_under_attack && robot.castle_under_attack_turn + 5 < robot.step) {
		robot.castle_under_attack = 0;
	}
};
var _castle_assign_mine_or_scout = function (robot) {
	if (__mod__ (robot.pilgrim_build_number, 2) == 1) {
		for (var iter_i = 0; iter_i < len (robot.karb_mine_occupancy_from_this_castle); iter_i++) {
			if (robot.karb_mine_occupancy_from_this_castle [iter_i] == -(1)) {
				robot.karb_mine_occupancy_from_this_castle [iter_i] = 0;
				var mine_pos = robot.karb_mine_locations_from_this_castle [iter_i];
				var comms = communications$2.encode_msg_without_direction (mine_pos [0], mine_pos [1]);
				return comms;
			}
		}
	}
	else if (__mod__ (robot.pilgrim_build_number, 2) == 0) {
		for (var iter_i = 0; iter_i < len (robot.fuel_mine_occupancy_from_this_castle); iter_i++) {
			if (robot.fuel_mine_occupancy_from_this_castle [iter_i] == -(1)) {
				robot.fuel_mine_occupancy_from_this_castle [iter_i] = 0;
				var mine_pos = robot.fuel_mine_locations_from_this_castle [iter_i];
				var comms = communications$2.encode_msg_without_direction (mine_pos [0], mine_pos [1]);
				return comms;
			}
		}
	}
};
var castle_build = function (robot, unit_type) {
	var pos_x = robot.me.x;
	var pos_y = robot.me.y;
	var occupied_map = robot.get_visible_robot_map ();
	var passable_map = robot.get_passable_map ();
	var directions$$1 = utility$a.random_cells_around ();
	for (var direction of directions$$1) {
		if (!(utility$a.is_cell_occupied (occupied_map, pos_x + direction [1], pos_y + direction [0])) && passable_map [pos_y + direction [0]] [pos_x + direction [1]] == 1) {
			return robot.build_unit (unit_type, direction [1], direction [0]);
		}
	}
	robot.log ('No space to build units anymore for castles');
	return null;
};
var castle_all_friendly_units = function (robot) {
	var all_units = robot.get_visible_robots ();
	var friendly_units = [];
	for (var unit of all_units) {
		if (unit.team == null) {
			friendly_units.append (unit);
		}
		else if (robot.me.team == unit.team) {
			friendly_units.append (unit);
		}
	}
	return friendly_units;
};

var __module_castles__ = /*#__PURE__*/Object.freeze({
    castle: castle,
    _castle_initial_check: _castle_initial_check,
    _castle_assign_mine_or_scout: _castle_assign_mine_or_scout,
    castle_build: castle_build,
    castle_all_friendly_units: castle_all_friendly_units
});

// Transcrypt'ed from Python, 2019-01-14 14:01:45
var castles = {};
var churches = {};
var communications$3 = {};
var constants$9 = {};
var crusaders = {};
var pilgrims = {};
var preachers = {};
var prophets = {};
var utility$b = {};
__nest__ (prophets, '', __module_prophets__);
__nest__ (preachers, '', __module_preachers__);
__nest__ (pilgrims, '', __module_pilgrims__);
__nest__ (crusaders, '', __module_crusaders__);
__nest__ (churches, '', __module_churches__);
__nest__ (castles, '', __module_castles__);
__nest__ (communications$3, '', __module_communications__);
__nest__ (constants$9, '', __module_constants__);
__nest__ (utility$b, '', __module_utility__);
var __name__$j = '__main__';
var find_unit_type = function (self, map$$1) {
};
var MyRobot =  __class__ ('MyRobot', [BCAbstractRobot], {
	__module__: __name__$j,
	step: __neg__ (1),
	unit_spawn_loc: null,
	current_move_destination: null,
	built_by_a_castle: 0,
	built_by_a_church: 0,
	our_castle_or_church_base: null,
	our_original_castle_location: null,
	pilgrim_type: 0,
	pilgrim_mine_ownership: null,
	mov_path_between_base_and_mine: null,
	mov_path_index: 0,
	pilgrim_in_danger: 0,
	has_made_random_movement: 0,
	pilgrim_scavenge_mine_location_list: [],
	pilgrim_scavenge_mine_occupancy_list: [],
	castle_unit_build_log: [],
	fuel_mine_locations_from_this_castle: [],
	fuel_mine_occupancy_from_this_castle: [],
	karb_mine_locations_from_this_castle: [],
	karb_mine_occupancy_from_this_castle: [],
	castle_health: null,
	pilgrim_assign_to_mine_type: 0,
	castle_under_attack: 0,
	castle_under_attack_turn: null,
	pilgrim_build_number: 0,
	church_unit_build_log: [],
	home_castle_location: null,
	is_targeting_robot_with_id: null,
	has_enemy_target_dict: dict ({}),
	is_fleeing_to_home_base: 0,
	has_unit_value: 1,
	get turn () {return __get__ (this, function (self) {
		self.step = __call__ (__iadd__, null, self.step, 1);
		var unit_type = __getitem__ (self.me, 'unit');
		if (__t__ (self.unit_spawn_loc === null)) {
			self.unit_spawn_loc = tuple ([__getitem__ (self.me, 'x'), __getitem__ (self.me, 'y')]);
		}
		(function () {
			var __accu0__ = self;
			return __call__ (__accu0__.castle_talk, __accu0__, self.me.unit);
		}) ();
		if (__t__ (__t__ (__eq__ (__mod__ (self.step, 200), 3)) && __eq__ (unit_type, constants$9.unit_castle))) {
			(function () {
				var __accu0__ = self;
				return __call__ (__accu0__.log, __accu0__, __add__ (__add__ (__add__ ('Total current karbonite is ', __call__ (str, null, self.karbonite)), ' turn '), __call__ (str, null, self.step)));
			}) ();
		}
		if (__t__ (__eq__ (unit_type, constants$9.unit_castle))) {
			return (function () {
				var __accu0__ = castles;
				return __call__ (__accu0__.castle, __accu0__, self);
			}) ();
		}
		else if (__t__ (__eq__ (unit_type, constants$9.unit_prophet))) {
			return (function () {
				var __accu0__ = prophets;
				return __call__ (__accu0__.prophet, __accu0__, self);
			}) ();
		}
		else if (__t__ (__eq__ (unit_type, constants$9.unit_pilgrim))) {
			return (function () {
				var __accu0__ = pilgrims;
				return __call__ (__accu0__.pilgrim, __accu0__, self);
			}) ();
		}
	});}
});
var robot = new MyRobot();