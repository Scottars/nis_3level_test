import numpy as np
import matplotlib.pyplot as plt

def sin_wave(start,zhouqi,midu,xdecimals,ydecimals):
    '''

    :param start: the fist value of the wave
    :param end:  the end value of the wave
    :param zhouqi:  the zhouqi range of the wave
    :param midu:  every zhouqi, there are how many points in this zhouqi
    :param xdecimals:  x decimals
    :param ydecimals: y decimals
    :return: the x array and the y array
    '''

    # 根据numpy的sin函数，生成对应的y的坐标。
    # y = np.sin(x)

    xout=[]
    yout=[]
    # for i in range(start,end,zhouqi):
    x = np.around(np.arange(start,start+zhouqi,midu),decimals=xdecimals)
    # y = np.where(x<start+0.5, x-start, 0)
    y = np.around(np.sin(x),decimals=ydecimals)

        # xout = np.append(xout, x)
        # yout = np.append(yout, y)
    return x,y





def triangle_wave(start,zhouqi,midu,xdecimals,ydecimals):
    '''

    :param start: the fist value of the wave
    :param end:  the end value of the wave
    :param zhouqi:  the zhouqi range of the wave
    :param midu:  every zhouqi, there are how many points in this zhouqi
    :return: the x array and the y array
    '''

    xout=[]
    yout=[]
    x = np.around(np.arange(start, start + zhouqi,  midu),decimals=xdecimals)
    # y = np.where(x<start+0.5, x-start, 0)
    y =np.around(np.where(x >= start + zhouqi/2, start + zhouqi - x, x - start),decimals=ydecimals)-1

    return x,y



def square_wave(start,zhouqi,midu,xdecimals,ydecimals):
    '''

    :param start: the fist value of the wave
    :param end:  the end value of the wave
    :param zhouqi:  the zhouqi range of the wave
    :param midu:  every zhouqi, there are how many points in this zhouqi
    :return: the x array and the y array
    '''
    xout = []
    yout = []
    x =np.around(np.arange(start, start + zhouqi,  midu),decimals=xdecimals)
    # y = np.where(x<start+0.5, x-start, 0)
    y =np.around(np.where(x >= start+ zhouqi/2, 1,0),decimals=ydecimals)

    return x, y



def sawtooth_wave(start,zhouqi,midu,xdecimals,ydecimals):
    '''

    :param start: the fist value of the wave
    :param end:  the end value of the wave
    :param zhouqi:  the zhouqi range of the wave
    :param midu:  every zhouqi, there are how many points in this zhouqi
    :return: the x array and the y array
    '''
    xout = []
    yout = []
    x =np.around(np.arange(start, start + zhouqi, midu),decimals=xdecimals)
    # y = np.where(x<start+0.5, x-start, 0)
    y =np.around(np.where(x >= start, start + zhouqi - x, x - start),decimals=ydecimals)-1

    return x,y


if __name__=='__main__':



    x,y=sin_wave(1,10,2,0.1,xdecimals=2,ydecimals=5)
    # for  i in range()
    plt.plot(x,y)
    plt.show()
    # x,y=triangle_wave(1,10,2,0.0001)
    # # for  i in range()
    # plt.plot(x,y)
    # plt.show()
    # x,y=square_wave(1,10,2,0.0001)
    # # for  i in range()
    # plt.plot(x,y)
    # plt.show()
    # x,y=swatooth_wave(1,10,2,0.0001)
    # # for  i in range()
    # plt.plot(x,y)
    # plt.show()
    #
