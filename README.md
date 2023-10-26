# Minimal_phase

### Short description

In this code I provide method of obtaining phase transfer function from modulation transfer function (MTF) for optical filter, given assumption that it is minimal phase (MPF).  I use Hendrik Bode approach and eventually plot the attenuation and phase transfer function (PhTF) .

### The aim of work

This code was provided to improve simulations of beams going through optical filters and other components of modern lasers. Previously phase dalays were not taken into account.

## Introduction

Optical transfer function (OTF) of arbitrary optical filter can be written as product of linear filter OTF and minimal phase filter OTF. The first one does not change amplitude, only phase of incoming beam, the second one changes both, the amplitude and phase in some specific way. When it comes to minimal phase filters, there is realtion between PhTF and MTF (modulus of OTF):

![wzor-1](https://github.com/Szymon975/Minimal_phase/assets/61831227/64f25263-e426-4c33-b1ae-6657b259777b)

where $"mathcal{H}"$ stands for Hilbert transform and $"H"$ is OTF. Hilbert transform is defined via equation:

![wzor-2](https://github.com/Szymon975/Minimal_phase/assets/61831227/45d238af-32a6-4bb9-a0bb-1f242a53794b),

where "p.v." stands for Cauchy principal value. What problem one might face while trying to implement these equations numerically?

![wzor-3](https://github.com/Szymon975/Minimal_phase/assets/61831227/a139a908-b811-4af9-88a0-edb8a144c17d)

As one might see on the upper picture, using the standard numerical technique generates some serious issues.

Because Butterworth filter is (MPF), we can use use eq. 2. We can obtain similar equation after adding few other assumptions. I show some fragment of article:  [Bode-relation-proof]([https://duckduckgo.com](https://arxiv.org/abs/1107.0071)https://arxiv.org/abs/1107.0071]): 

![Bode-relation-proof](https://github.com/Szymon975/Minimal_phase/assets/61831227/5124b39b-548a-4344-959d-648c494e4d58)

There are 

