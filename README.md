# PyAutoClicker

一个用Python写的简易连点器。
> 这个程序使用由``ctypes``提供的Windows API接口，所以它只在Windows上可用。

现在这个程序的能干的很少，无非就是不停地点鼠标。我会继续写更多的代码(bug)，目标是：

1. 尝试解决点击间隔过低而造成的鼠标卡顿
2. 把`pynput`这个依赖解决掉，这样就不用装库了（现在已经解决了点击与键盘，还差监听）
3. 尝试优化点击间隔的准确性（提高`time.sleep`的准确性，或用其它方法代替）
4. 支持更改键位

这个可以用来玩MC，但我不建议你这么做（菜就多练...

现在只有简体中文可用

# PyAutoClicker

A simple auto clicker written in Python.

> This program uses Windows API in ``ctypes``, so it is only available on Windows.

This program can't do many things currently. All is to click the mouse again and again. I'll continue to write more code
(bugs), the goals are:

1. Try to the lag caused by the low clicking interval
2. Remove the dependency `pynput`, so that we won't need to install libs any more (now I have implemented mouse clicking
   and keyboard, mouse event listener is on the way)
3. Try to optimize the accuracy of clicking interval (improve `time.sleep`'s accuracy, or use other methods)
4. Modifiable keys

This can be used to play Minecraft, but I don't suggest you to do this. (practise more if you're a noob...

Only available in Chinese-Simplified currently.
