__author__ = 'Konrad'
import matplotlib.pyplot as plt
import numpy

H=10
#v0x=10
m=1.
#wspop=0.0
#dt=0.0000001
# N=10
g=9.81

def rzut(dt,N,wspop,v0x):
    vx=[]
    vy=[]
    x=[]
    y=[]
    t=[]
    vx.append(v0x)
    vy.append(0)
    x.append(0)
    y.append(H)
    t.append(0)
    ec=[]
    ec.append(m*g*H+v0x**2/2)

    for i in range(N):
        fx=-wspop*vx[i]**2
        fy=-g+wspop*vy[i]**2
        print(fy)
        print(i)
        vx.append(vx[i]+fx/m*dt)
        vy.append(vy[i]+fy/m*dt)
        x.append(x[i]+vx[i]*dt)
        y.append(y[i]+vy[i]*dt)
        t.append(i+1)
        ec.append(m*g*y[i]+(m*(vx[i]**2+vy[i]**2)/2))


    tprim=[i*dt for i in t]
    #plt.plot(tprim,vy,label='$wsp. oporu = %g$ , $V0 = %g$' % (wspop,v0x))
    plt.plot(tprim,ec,label='$Krok czasowu = %g$ , metoda Eulera' % dt)
    # plt.plot(x,y,label='$Krok czasowu = %g$ , metoda Eulera' % dt)
    #plt.show()
    #plt.plot(x,y)
def rzut_rk4(dt,N,wspop,v0x):
    vx=[]
    vy=[]
    x=[]
    y=[]
    t=[]
    vx.append(v0x)
    vy.append(0)
    x.append(0)
    y.append(H)
    t.append(0)

    ec=[]
    ec.append(m*g*H+v0x**2/2)
    for i in range(N):
        k1x=dt*fx(t[i],x[i],vx[i])
        k1vx=dt*fvx(t[i],x[i],vx[i],wspop)
        k2x=dt*fx(t[i]+dt/2,x[i]+k1x/2,vx[i]+k1vx/2)
        k2vx=dt*fvx(t[i]+dt/2,x[i]+k1x/2,vx[i]+k1vx/2,wspop)
        k3x=dt*fx(t[i]+dt/2,x[i]+k2x/2,vx[i]+k2vx/2)
        k3vx=dt*fvx(t[i]+dt/2,x[i]+k2x/2,vx[i]+k2vx/2,wspop)
        k4x=dt*fx(t[i]+dt,x[i]+k3x,vx[i]+k3vx)
        k4vx=dt*fvx(t[i]+dt,x[i]+k3x,vx[i]+k3vx,wspop)

        k1y=dt*fy(t[i],y[i],vy[i])
        k1vy=dt*fvy(t[i],y[i],vy[i],wspop)
        k2y=dt*fy(t[i]+dt/2,y[i]+k1y/2,vy[i]+k1vy/2)
        k2vy=dt*fvy(t[i]+dt/2,y[i]+k1y/2,vy[i]+k1vy/2,wspop)
        k3y=dt*fy(t[i]+dt/2,y[i]+k2y/2,vy[i]+k2vy/2)
        k3vy=dt*fvy(t[i]+dt/2,y[i]+k2y/2,vy[i]+k2vy/2,wspop)
        k4y=dt*fy(t[i]+dt,y[i]+k3y,vy[i]+k3vy)
        k4vy=dt*fvy(t[i]+dt,y[i]+k3y,vy[i]+k3vy,wspop)



        # y.append(y[i]+dt*(k1+2*k2+2*k3+k4)/6)
        vy.append(vy[i]+(k1vy+2*k2vy+2*k3vy+k4vy)/6)
        vx.append(vx[i]+(k1vx+2*k2vx+2*k3vx+k4vx)/6)
        y.append(y[i]+(k1y+2*k2y+2*k3y+k4y)/6)
        x.append(x[i]+(k1x+2*k2x+2*k3x+k4x)/6)

        t.append(i+1)
        ec.append(m*g*y[i]+(m*(vx[i]**2+vy[i]**2)/2))
    tprim=[i*dt for i in t]
    #plt.plot(x,y,label='$Krok czasowu = %g$ , metoda RK4' % dt)
    plt.plot(tprim,ec,label='$Krok czasowu = %g$ , metoda RK4' % dt)




def fx(t,x,vx):
    return vx
def fvx(t,x,vx,wsp):
    return -wsp*vx**2
def fy(t,y,vy):
    return vy
def fvy(t,y,vy,wsp):
    return -g+wsp*vy**2

# plt.plot(x,y)
# plt.show()
# plt.plot(t,x)
# plt.show()
# plt.plot(t,y)
# plt.show()
# plt.plot(t,vx)
# plt.show()
# plt.plot(t,vy)

# plt.plot(t,ec)
# plt.show()
#
# print(max(ec)," ",min(ec))
# print
#

# rzut(0.0001,20000,0,10)
# rzut(0.0001,20000,0.2,10)
# rzut(0.0001,20000,0.4,10)
# rzut(0.0001,20000,0.6,10)
# rzut(0.0001,20000,0.8,10)
# rzut(0.0001,20000,1,10)

# rzut(0.0001,20000,0.6,30)
# rzut(0.0001,20000,1,30)
# plt.ylim(-10,10)
# plt.xlim(0,70)
# rzut(0.0001,20000,0.3,25)
# rzut(0.0001,20000,0.7,25)



t=numpy.linspace(0,10,1000)
x=[10*i  for i in t]
y=[H-g*i**2/2 for i in t]
# plt.plot(x,y)
# plt.xlabel("Czas")
# plt.ylabel("Predkosć Y")
# plt.xlabel("Czas")
# plt.ylabel("Energia calkowita")
# plt.legend(loc=3)

rzut_rk4(0.01,100,0,10)
rzut(0.01,100,0,10)
plt.xlabel("Czas")
plt.ylabel("Energia calkowita")
plt.legend(loc=3)
plt.show()