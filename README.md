# Minimal_phase

### Short description

In this code I provide method of obtaining phase transfer function from modulation transfer function (MTF) for optical filter, given assumption that it is minimal phase (MPF).  I use Hendrik Bode approach and eventually plot the attenuation and phase transfer function (PhTF) .

### The aim of work

This code was provided to improve simulations of beams going through optical filters and other components of modern lasers. Previously phase dalays were not taken into account.

## Introduction

Optical transfer function (OTF) of arbitrary optical filter can be written as product of linear filter OTF and minimal phase filter OTF. The first one does not change amplitude, only phase of incoming beam, the second one changes both, the amplitude and phase in some specific way. When it comes to minimal phase filters, there is realtion between PhTF and MTF (modulus of OTF):

![wzor-1](https://github.com/Szymon975/Minimal_phase/assets/61831227/64f25263-e426-4c33-b1ae-6657b259777b)

where $\mathcal{H}$ stands for Hilbert transform and $H$ is OTF. Hilbert transform is defined via equation:

![wzor-2](https://github.com/Szymon975/Minimal_phase/assets/61831227/45d238af-32a6-4bb9-a0bb-1f242a53794b),

where "p.v." stands for Cauchy principal value. What problem one might face while trying to implement these equations numerically?

![wzor-3](https://github.com/Szymon975/Minimal_phase/assets/61831227/a139a908-b811-4af9-88a0-edb8a144c17d)

As one might see on the upper picture, using the standard numerical technique generates some serious issues.

Because Butterworth filter is (MPF), we can use use eq. 2. We can obtain similar equation after adding few other assumptions. I show some fragment of article:  [Bode-relation-proof]([https://duckduckgo.com](https://arxiv.org/abs/1107.0071)https://arxiv.org/abs/1107.0071]): 

![Bode-relation-proof](https://github.com/Szymon975/Minimal_phase/assets/61831227/5124b39b-548a-4344-959d-648c494e4d58)

There are few reasons for troubles related to this approach:

1. We are not able to integrate numerically to infinity. In ideal case, we would like to integrate to some $\omega' (\omega)$ such that integrand is negligibly small and doesn't change value with $\omega$, but it would be troublesome to implement. Deciding on constant cut-off $\omega'$, for $\omega$ approaching cut-off $\omega'$, integrand is much bigger than for small $\omega$. The result is approximately fine for $\omega$ much smaller than cut-off $\omega'$.

2. Cauchy principal value is troublesome to implement. Notice that we have to neglect values of integrand in points which depend on $\omega$. There exist *hilbert* from *scipy.signal*, implementation by hand is complicated.

There exists solution to all these problems. Integrating over variable $\omega'/\omega$ instead of $\omega'$ for large and constant cut-off $\omega'/\omega$, will guarantee $\omega \ll \omega'$. Secondly, after making substitution $u = \textnormal{log}(\omega'/ \omega)$, it turns out that one can get rid of Cauchy principal value before integral, because the neglected part of integral is measure zero. 

![wzor-5](https://github.com/Szymon975/Minimal_phase/assets/61831227/02d4311b-c56f-4895-84b4-d81c7842ef57)

In the next step of the article ![Bode-relation-proof](https://github.com/Szymon975/Minimal_phase/assets/61831227/5124b39b-548a-4344-959d-648c494e4d58), one performs integration by parts and adding few additional assumptions on boundary terms:

![wzor-6](https://github.com/Szymon975/Minimal_phase/assets/61831227/9c062d23-ccda-4c5b-90f6-471dbe22d4b7),

after which one obtains equation proven in 1937, analysed in doctoral thesis of **Hendrik Wade Bode**.

![download](https://github.com/Szymon975/Minimal_phase/assets/61831227/a44b09ad-e0d3-403d-86bd-13ba103217a9).

In Bode's original article ( ![Bode-relation](https://linearaudio.nl/sites/linearaudio.net/files/Bode%201940%20monograph%20gain%20and%20phase%20in%20fb%20amps%20searchable.pdf), Bode draws graphs named after him (Bode graphs) for various transfer functions using described equation.

This equation has some weak points, which consequences I sucessfully avoided.

1. Due to the substitution $v --> \textnormal{exp}(u)$ some very big numbers are generated. Notice that we are still integrating to very big $omega'$s, with the difference that regular distribution of points $u$ in Riemann sum translates to fewer points $\omega'$ before the substitution. I had this problem only plotting *dawson* and after making use of *mpmath*, after approximately thirty seconds I obtained plot for 300 points.

2. Less apparent symmetry - $$G'(v) = G(v-a)$, where "a" is some central $\omega/\omega_0$, PhTF should be translated analogously. Reason for this problem to occur is due to taking into account only positive $\omega'$s in integration because of previous change of variables - argument of logarithm must be positive.

![download](https://github.com/Szymon975/Minimal_phase/assets/61831227/297e743b-d127-4070-88ab-8af4f7b92dd3)

Solution to this problem is different definition of variables: $$v_0 = ω/ω_0 -a, \ v' = ω/ω_0 - a, \  u_0 = log(v_0), \ u' = log(v')$$.

In my code, we take function centered in zero and then we type in value of $a$ and obtain function adequately translated with added antisymmetric part , which gives another integral on negative $\omega$s, then we have $-v$ in arguments of differently defined $u$s.

Used packages:

from __future__ import with_statement
import matplotlib.pyplot as plt
import numpy as np
import math as m
from mpmath import *
from scipy.signal import hilbert
from sympy import *
from sympy import lambdify
from scipy import special





