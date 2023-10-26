from __future__ import with_statement
import matplotlib.pyplot as plt
import numpy as np
import math as m
from mpmath import *
from scipy.signal import hilbert
from sympy import *
from sympy import lambdify
from scipy import special

x, y = symbols('x y', positive=True)
n = symbols('n', real=True)
init_printing(use_unicode=True)

class Bode_Graphs:
    def __init__(self, MTF, limit, samples, central_freq = 0, type = None, hilbert = False, higher_precision = False):
        self.MTF = MTF
        self.limit = limit
        self.samples = samples
        self.central_freq = central_freq
        self.type = type
        self.hilbert = hilbert
        self.higher_precision = higher_precision
        self.step_u = 2 * np.log(self.limit) / (self.samples - 1)
        self.domain_u = np.arange(-np.log(self.limit), np.log(self.limit-self.central_freq) + self.step_u, self.step_u)
        self.domain_f_u = np.exp(self.domain_u)
        self.step_freq = self.limit / (self.samples - 1)
        self.domain_freq = np.arange(0, self.limit + self.step_freq, self.step_freq)
        self.hilbert_domain = np.concatenate((-self.domain_freq[1:][::-1], self.domain_freq))
        self.a = lambdify(x, simplify(-log(abs(self.MTF(x)))), "scipy")
        if self.higher_precision:
            self.expr = lambdify((x,y), simplify(-log(abs(self.MTF(exp(x + y))))), "mpmath")
        else:
            self.expr = lambdify((x, y), simplify(-log(abs(self.MTF(exp(x + y))))), "scipy")

    def integrand(self, u, u_o):
        return -m.pi ** (-1) * (self.expr(u, u_o + self.step_u) - self.expr(u, u_o)) /self.step_u * np.log(np.tanh(abs(u / 2)))

    def freq_domain(self):
        return np.exp(self.domain_u) + self.central_freq
    def row(self,x, i=integrand):
        return [i(self, y, x)*self.step_u for y in self.domain_u]

    def integrate(self, r = row, i=integrand):
        if self.higher_precision:
            return np.array([np.sum(r(self,x)) for x in self.domain_u], dtype = float)
        else:
            return np.array([np.sum(self.step_u * i(self, self.domain_u, x)) for x in self.domain_u], dtype = float)


    def hilbert_func(self):
        return -np.imag(hilbert(self.a(self.hilbert_domain-self.central_freq)))

    def plot(self, h=hilbert_func, i=integrate):
        fig, (ax1, ax2) = plt.subplots(2, 1)
        fig.suptitle("Bode plots" +  f" {self.type}")
        a,b,c = -np.max(i(self)), np.max(i(self)), np.max(self.domain_f_u)
        ax1.set_ylim([a - 0.2*abs(a), b + 0.2*abs(b)])
        ax1.set_xlim([0, c + 0.2*abs(c)])
        if self.hilbert:
            ax1.plot(self.domain_freq, h(self)[self.samples-1:], label='Hilbert transform method', color='r')
        ax1.plot(self.domain_f_u + self.central_freq, i(self), label='Proposed method', color='b')
        ax1.plot(-self.domain_f_u + self.central_freq, -i(self),  color='b')
        if self.type == "lorentz":
            ax1.plot(self.domain_freq, np.arctan(self.domain_freq - self.central_freq), label='Correct solution', color='g')
        if self.type == "dawson":
            ax1.plot(self.domain_freq, np.arctan(special.erfi(self.domain_freq - self.central_freq)), label='Correct solution', color='g')
        ax1.set(xlabel='f/f_o', ylabel='phi [rad]')
        #ax1.set_xscale('log')
        ax1.grid()
        ax1.legend()
        ax2.plot(self.domain_f_u, 20*m.log(e,10)*self.a(self.domain_f_u - self.central_freq), color='g')
        ax2.set(xlabel='f/f_o', ylabel='Attenuation [dB]')
        #ax2.set_xscale('log')
        ax2.grid()

        fig.set_figheight(7)
        fig.set_figwidth(9)
        #plt.savefig(f" {self.type}")
        plt.show()


lorentz = Bode_Graphs(lambda t: 1 / (t** 2 + 1) ** (1 / 2), 100, 1000, central_freq = 10,  type = "lorentz", hilbert = True)
heaviside = Bode_Graphs(lambda t: exp(-1 - Heaviside(t - 1, 1)), 10, 1000, type = "heaviside")
gaussian = Bode_Graphs(lambda t: exp(-t** 2 / 2), 10, 1000, type =  "gaussian")
logarithm = Bode_Graphs(lambda t: 1 / t, 100, 1000, type = "logarithm")
dawson = Bode_Graphs(lambda t: (exp(-2*t**2) + exp(-2*t**2)*(erfi(t)**2))**(1/2), 100, 100, central_freq = 10, type = "dawson", higher_precision = True)
dawson.plot()



