# Feeling

![Feeling in action](https://raw.githubusercontent.com/davep/feeling/main/img/feeling.png)

## Introduction

Feeling is designed to be a simple terminal-based feelings tracker,
providing a simple command line interface for recording a feeling at any
time, and an application (built with
[Textual](https://textual.textualize.io/) for reviewing the recorded
feelings.

## Installation

Feeling can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
$ pipx install feeling-cli
```

**NOTE:** The package name (`feeling-cli`) is slightly different from the
actual application name because the package name wasn't available via PyPi.

## Usage

Feeling is one command that is split into two parts. There is a simple
command line interface for recording a feeling, and a full-screen user
interface for looking back over what's been recorded and how it all fits
together and flows.

### Recording a feeling

To record a feeling, on the command line, just type:

```sh
$ feeling <rating> <description>
```

So, for example:

```sh
$ feeling good I installed feeling and will use it to track how I feel
```

This will make a record for the moment that the feeling is recorded. You can
do this as many times as you like. The more you record, the more you'll
build up a record of your day, month, year...

Feeling takes a simple approach of having five levels of feeling, and it
will also look for various words that map to those levels (I'll add to them
over time). The levels and the words associated with them are:

### -2

Very low. Words associated with this level are:

- Horrible
- Lowest
- Rubbish
- Worst

### -1

Low. Words associated with this level are:

- Blah
- Down
- Downbeat
- Low
- Meh
- Negative

### 0

Neutral. Words associated with this level are:

- Flat
- Level
- Neutral
- Ok
- Okay

### 1

Good. Words associated with this level are:

- Better
- Fine
- Good
- Positive
- Upbeat

### 2

Very good. Words associated with this level are:

- Amazing
- Awesome
- Elated
- Excellent
- Fantastic
- Great
- Wonderful

### Viewing your feeling history

To view the history simply run `feeling` with no parameters. For now this is
just a simple read-only interface; you can look through years, months and
days, and see the colour-coded overall record for each. In time I aim to add
more features (such as the ability to go back and edit, or remove entries).)

## Data

The data for the application is held in the appropriate [XDG home data
directory for your
platform](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).
On Unix-like systems expect to find it in `~/.local/share/feelings`.

## TODO

This is a very early release, where I'm just testing out the basic idea. My
aim is that the data format is already stable (it is quite simple), but the
user interface of the main application may change significantly as I play
around with it.

Things I aim to do:

- [ ] Expand the list of words for the feelings scale.
- [ ] Generally improve the main application user interface.
- [ ] Add the ability to edit items within the main application.
- [ ] Add the ability to remove items within the main application.

## Licence

Feeling - A simple terminal-based feelings tracker  
Copyright (C) 2023-2024 Dave Pearson

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

[//]: # (README.md ends here)
