#class used for LU decomposition
#a:2d array coffecient matrix
#b:1D array of values
from LU.FloatConverter import FloatConverter


class LUDecomposerService:
    def __init__(self,a,b,converter:FloatConverter):
        self.__a=a
        self.__b=b
        self.converter=converter
    @property
    def a(self):
        return self.__a
    @a.setter
    def a(self,value):
        self.__a=value
    @property
    def b(self):
        return self.__b
    @b.setter
    def b(self,value):
        self.__b=value
    #Scaling and pivoting
    def findScalers(self):
        n=len(self.__a)
        o=[0]*n
        s=[0]*n
        for i in range (0,n):
            o[i]=i
            s[i]=abs(self.__a[i][0])
            for j in range(1,n):
                if(abs(self.__a[i][j])>s[i]):
                    s[i]=abs(self.__a[i][j])
        return o,s

    def pivoting(self,scalers,o, k):
            pivot = k
            N=len(self.__a)
            biggestPivot = self.converter.convert(abs(self.__a[o[k]][k]) / float(scalers[k]))
            for i in range(k + 1, N):
                temp = self.converter.convert(abs(self.__a[o[i]][k]) / float(scalers[o[i]]))
                if (temp > biggestPivot):
                    pivot = i
                    biggestPivot = temp
            temp=o[pivot]
            o[pivot]=o[k]
            o[k]=temp
    #Doolittle method
    def forward_eliminate(self):
        n=len(self.__a)
        o, s = self.findScalers()
        for k in range(0,n-1):
            self.pivoting(s,o,k)
            for i in range(k+1,n):
                mult=self.converter.convert(float(self.__a[o[i]][k])/float(self.__a[o[k]][k]))
                self.__a[o[i]][k]=mult
                for j in range(k+1,n):
                    self.__a[o[i]][j]=self.converter.convert(self.__a[o[i]][j]-self.converter.convert(mult*self.__a[o[k]][j]))
        return o

    def forwardSubstitution(self,o):
        n=len(self.__a)
        y=[0]*n
        y[o[0]] = self.__b[0]
        for i in range(1,n):
            value=self.__b[o[i]]
            for j in range(0,i):
                value=self.converter.convert(value-self.converter.convert(self.__a[o[i]][j]*y[o[j]]))
            y[o[i]] = value
        return y

    def backSubstitution(self,y,o):
        n=len(self.__a)
        x = [0.0] * n
        x[n-1]=self.converter.convert(float(y[o[n-1]])/float(self.__a[o[n-1]][o[n-1]]))
        for i in range(n-2,-1,-1):
            sum=0
            for j in range(i+1,n):
                sum=self.converter.convert(sum+self.converter.convert(self.__a[o[i]][j]*x[j]))
            x[i]=self.converter.convert(float(y[o[i]]-sum)/float(self.__a[o[i]][i]))
        return x
    #Crout's method
    def croutForwardEliminate(self):
        n = len(self.__a)
        #getting u12,u13,...
        for i in range(1,n):
            self.__a[0][i]=self.converter.convert(self.__a[0][i]/float(self.__a[0][0]))
        #rest of elements i<j:upper otherwise lower
        for j in range(1,n):
            for i in range(1,n):
                sum=0
                k=0
                m=0
                while(k<j and m<i):
                    sum = self.converter.convert(sum+self.converter.convert(self.__a[i][k]*self.__a[m][j]))
                    k=k+1
                    m=m+1
                if(i<j):
                    self.__a[i][j] = self.converter.convert(float((self.__a[i][j] - sum)) / self.__a[i][i])
                else:
                    self.__a[i][j] = self.converter.convert(self.__a[i][j] - sum)
    def croutBackSubtitution(self, y):
        n = len(self.__a)
        x=[0.0]*n
        x[n - 1] = y[n - 1]
        for i in range(n - 2, -1, -1):
            value = y[i]
            for j in range(i+1, n):
                value = self.converter.convert(value - self.converter.convert(self.__a[i][j] * x[j]))
            x[i] = value
        return x
    def croutForwardSubstitution(self):
        n = len(self.__a)
        y = [0.0] * n
        y[0] = self.converter.convert(float(self.__b[0]) / float(self.__a[0][0]))
        for i in range(1, n):
            sum = 0
            for j in range(0,i):
                sum = self.converter.convert(sum + self.converter.convert(self.__a[i][j] * y[j]))
            y[i] = self.converter.convert(float(self.__b[i] - sum) / float(self.__a[i][i]))
        return y
    #Controller functions
    def croutDecomposition(self):
        self.croutForwardEliminate()
        y = self.croutForwardSubstitution()
        x=self.croutBackSubtitution(y)
        return x
    def DooLittle_Decomposition(self):
        o=self.forward_eliminate()
        y = self.forwardSubstitution(o)
        x=self.backSubstitution(y,o)
        return x



