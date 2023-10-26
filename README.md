# Minimal_phase

### Short description

In this code I provide method of obtaining phase transfer function from modulation transfer function (MTF) for optical filter, given assumption that it is minimal phase.  I use Hendrik Bode approach and eventually plot the attenuation and phase transfer function (PhTF) .

### The aim of work

This code was provided to improve simulations of beams going through optical filters and other components of modern lasers. Previously phase dalays were not taken into account.

## Introduction

Optical transfer function (OTF) of arbitrary optical filter can be written as product of linear filter OTF and minimal phase filter OTF. The first one does not change amplitude, only phase of incoming beam, the second one changes both, the amplitude and phase in some specific way. When it comes to minimal phase filters, there is realtion between PhTF and MTF (modulus of OTF) { a }: 

![Tux, the Linux mascot](C:\Users\ACER\Desktop\portfolio\github_images\wzor_1.png)
