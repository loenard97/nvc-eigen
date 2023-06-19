<div align="center">

# nvc-eigen
NV-center Hamiltonian library

![](https://img.shields.io/github/last-commit/loenard97/nvc-eigen?&style=for-the-badge&logo=github&color=3776AB)
![](https://img.shields.io/github/repo-size/loenard97/nvc-eigen?&style=for-the-badge&logo=github&color=3776AB)

</div>


# 📖 Library
This library contains helper functions for solving the NV-center Hamiltonian:
```math
H = H_{ss} + g_s H_B  = 
\left( \begin{matrix}
    D & 0 & E \\
    0 & 0 & 0 \\
    E & 0 & D \\
\end{matrix} \right) 
+
\left( \begin{matrix}
    B_z                              & \frac{1}{\sqrt{2}}(B_x + i B_y)  & 0                                \\
    \frac{1}{\sqrt{2}}(B_x - i B_y)  & 0                                & \frac{1}{\sqrt{2}}(B_x + i B_y)  \\
    0                                & \frac{1}{\sqrt{2}}(B_x - i B_y)  & -B_z                             \\
\end{matrix} \right)
```

# 🔍 Visualization tool
Additionally a visualization tool that plots the resulting ODMR spectrum is included.

![](/screenshots/screenshot.png)
