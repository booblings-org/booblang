# 1. Documentation
## 1.1. Lexing
### 1.1.1. Example Code
In the following we will walk through a lexing of a first example. In our language file we have written this line:

```
let a be 130
```

This line represents **one** *action*. For each *action* in the lexer will go though steps that will be described next. The amount of required steps will vary between different *actions*.

### 1.1.2. Example Run: Assignment
#### 1.1.2.1. *First Step*
As the lexer scans the data given by the analyzer from the example above, he will find the first set of characters `let` and creates a new *Token* which will look like this:

```
Token {
    name: 'let',
	properties: {
		type: 'assignment',
		struct: [{
			class: 'Token',
			type: ['assignment'],
			done: true
		},{
			class: 'Name',
			type: ['identifier'],
			done: false
		},{
			class: 'Token',
			type: ['expectation'],
			done: false
		},{
			class: 'Expr',
			type: ['value','term'],
			done: false
		}],
		allow: ['string'],
		valid: true,
		complete: false
	}
}
```

Wow thats some chunk of code, lets explain what is going on there.

**`Token {}`** is a *class* which holds all required information, you need to explain a single *action*. If we would add a second line similar to the one in the example, we would need two *Token* instances to represent the code. A list of *classes* can be found later in the documentation.

The key **`name: ''`** tells us how the *Token* is called. As it is basically a copy of the code's content, the value `'let'` is assigned.

Next we have **`properties: {}`** which holds information about what the *Token* does and how the context it is used in, must look like. It also says, whether the *Token* is complete and fullfills all requirements or contains an error.

Inside, we have **`type: ''`** which tells us the *type* of the token. Here the value of `type` is `'assignment'` as the *Token* `let` indicated an *assignment* of a variable. A list of token types can be found later in the documentation.

**`struct: []`** shows how the following code must look like to complete the *action*. Its value is an array of objects with the keys `class: ''` which shows the required *class* of the character set, `type: []` which is a list of possible types and `done: false` which is set to `true` if this structure was found in the sets of the current *action*.

**`allow: []`** is a list of allowed characters. Here we only want the *assignment* *Token* to be a string. In other cases, more types could be allowed.

**`valid: true`** tells, if the *action* is valid or not. It can just be set to `true` if every requirement is valid as well. Those would include `allow: []` as well as `class: ''` and `type: []` from `struct: []`.

Finally, **`complete: false`** sets to `true` if every `done: false` from `struct: []` was set to `true`, too.

#### 1.1.2.2. *Second Step*
Since the *Token* we created above still says `complete: false`, we append the new key `next: [{}]` to it:

```
Token {
	name: 'let',
	properties: {
		...
		complete: false
	},
	next: [{}]
}
```

#### 1.1.2.3. *Third Step*
To be able to complete the *action*, we need to scan the next set of characters. In our code example we find `a` to be the next set. A comparison with the *Tokenlist* yields that `a` is not a *Token*, so it must be either a *Name* or an *Expr*. After checking if the set contains any *Operators*, which is not the case, we find `a` to be of the *class* *Name*. As this is exactly what we need, we can construct:

```
Name {
	name: 'a',
	properties: {
		type: 'identifier',
		struct: [{
			class: 'Name',
			type: ['identifier'],
			done: true
		}],
		allow: ['string'],
		valid: true,
		complete: true
	}
}
```

As you can see, the properties `valid` and `complete` are already set to `true`. This is because an *identifier* is allowed to appear alone as it doesn't require a specific structure around it, as an *assignment* does for example.

#### 1.1.2.4. *Fourth Step*
Now we insert the content of the just created *Name* into `next: [{}]` from before, so that the whole thing now looks like this:

```
Token {
	name: 'let',
	properties: {
		type: 'assignment',
		struct: [{
			class: 'Token',
			type: ['assignment'],
			done: true
		},{
			class: 'Name',
			type: ['identifier'],
			done: false
		},{
			class: 'Token',
			type: ['expectation'],
			done: false
		},{
			class: 'Expr',
			type: ['value','term'],
			done: false
		}],
		allow: ['string'],
		valid: true,
		complete: false
	},
	next: [{
		name: 'a',
		properties: {
			type: 'identifier',
			struct: [{
				class: 'Name',
				type: ['identifier'],
				done: true
			}],
			allow: ['string'],
			valid: true,
			complete: true
		}
	}]
}
```

You can see, that the second structure requirement in `struct: []` of our *Token* now is done, as we just added a *Name* of the type *identifier* and we can change the corresponding key to `done: true`.

#### 1.1.2.5. *Fifth Step*
Our *Token* is still not completed yet, so as you might expect, we will have to add the next *class* to it. In case you wondered why `next: []` is an array, now we will make use of it.


## 1.2 Lists
### 1.2.1 Classes, Types and Allowed

class|types|allowed|examples||
-|-|-|-|-
**Token**|assignment|string|let|give
||expectation|string|equals|be
||iteration|string|until|while
**Name**|identifier|string, punctuation|foo_bar|pi
**Expr**|value|number, punctuation|3.141|1691232
||term|number, operator|23 - 14|55 / 3 + 7
**Symbol**|binding|parenthesis|)|{
||separation|punctuation|;|"
