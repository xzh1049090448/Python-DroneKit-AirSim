import run1, run2, run3, run4, run5, run6, run7, run8, run9
from multiprocessing import Process

uav = []
processes = []


def target1():
    run_oj = run1.Run(1)
    uav.append(run_oj)
    run_oj.start()


def target2():
    run_oj = run2.Run(2)
    uav.append(run_oj)
    run_oj.start()


def target3():
    run_oj = run3.Run(3)
    uav.append(run_oj)
    run_oj.start()


def target4():
    run_oj = run4.Run(4)
    uav.append(run_oj)
    run_oj.start()


def target5():
    run_oj = run5.Run(5)
    uav.append(run_oj)
    run_oj.start()


def target6():
    run_oj = run6.Run(6)
    uav.append(run_oj)
    run_oj.start()


def target7():
    run_oj = run7.Run(7)
    uav.append(run_oj)
    run_oj.start()


def target8():
    run_oj = run8.Run(8)
    uav.append(run_oj)
    run_oj.start()


def target9():
    run_oj = run9.Run(9)
    uav.append(run_oj)
    run_oj.start()


if __name__ == '__main__':

    pr1 = Process(target=target1, name="1th controller")
    processes.append(pr1)
    pr2 = Process(target=target2, name="2th controller")
    processes.append(pr2)
    pr3 = Process(target=target3, name="3th controller")
    processes.append(pr3)
    pr4 = Process(target=target4, name="4th controller")
    processes.append(pr4)
    pr5 = Process(target=target5, name="5th controller")
    processes.append(pr5)
    pr6 = Process(target=target6, name="5th controller")
    processes.append(pr6)
    pr7 = Process(target=target7, name="5th controller")
    processes.append(pr7)
    pr8 = Process(target=target8, name="5th controller")
    processes.append(pr8)
    pr9 = Process(target=target9, name="5th controller")
    processes.append(pr9)
    print(len(processes))
    for i in range(9):
        processes[i].start()
        print("uav " + str(i + 1) + " process start")
