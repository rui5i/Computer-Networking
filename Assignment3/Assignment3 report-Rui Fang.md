## Assignment3 report-Rui Fang

### Testing screenshots:

1. Run demo_receiver to see what received in each packet:

   ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 11.01.14.png)

2. Test dummy first:

   First run `python3 demo_reciver.py dummy` in receiver window(right), then run `python3 demo_sender.py dummy` to text dummy. 

   ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 11.21.37.png)

We can see some bit errors in receiver window. 

3. Test stop and wait:

   First run `python3 demo_reciver.py ss` in receiver window, then run` python3 demo_sender.py ss`:

   ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 13.35.48.png)

Then test `python3 file_sender.py ss test.txt` and `python3 file_receiver.py ss output.txt`

![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 13.41.11.png)

file output successful.

4. Test go back n:

   Test demo:

   ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 13.43.27.png)

We can see some packets go back and resend.

​	Test file_sender/receiver:	![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 13.44.24.png)

### Description:

1. Stop and wait:

   - Sender send one packet at a time, when making packet, use check_sum helper to make a packet with data_type, sequence_number, check_sum, payload. In the meantime set a timer wait for ack.

     If received the ack, then sending the packet that ack told. If doesn't received ack in the time period, resend the previous one.

   - Receiver when receive a packet, check the check sum first, to see if it's a complete packet. If it's a complete packet, look at the data type, if it's ack then that is sender received. If it's data then it's receiver received. If the packet is correct then send the ack and stop the timer. Otherwise reset the expected sequence to be last one.

2. Go back N:

   - Sender has a window. When sending packet, send window size packets at a time. Set a timer and wait for expected ack. When received a ack msg, keep sending the following packets told by msg. If times out and don't receive the expected ack, then resend the whole window size from last correct sequence number. 
   - Receiver receive packets, first do the check sum to see if it's a correct packet, if it is, then make the sequence number + 1, then receiver send the correct sequence number to sender. If the expected number > sequence that means all packets are received successfully and can stop the timer. 

### Compare performance:

1. The high and low error rate：

   - compare with itself:

     ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 15.04.47.png)

     When change the error rate to 0.3, the send time is longer than before. Because no matter what protocol, when error happens, they need to do the resend. So the higher of the error rate, the longer of the sending time.

   - SS vs GBN:

     When error rate is 0.3: the ss is lower than gbn(I don't know why, maybe the packet number is not large enougth and also my window size is 5. So overall gbn perform better.):

     ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 15.07.06.png)

     ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 15.07.57.png)

     Changing error rate to 0.5:

     ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 15.10.27.png)

     ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 15.11.47.png)

     When changing the error rate to 0.5, the gbn becomes worse. I believe if the error rate keeps rising, the go back n would be much more worse than stop and wait. Because it needs to resent multiple packets at a time while ss only need to resend one.

2. Long and short RRT (you may use VMs located in different places to simulate the RRT, e.g. connections between Oregon and California should have longer RRT than that between Oregon and Beijing)

   My two instances are based on us east coast and west coast.

   ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 15.37.32.png)

   ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 15.50.41.png)

   ![](/Users/Rui/Desktop/Screen Shot 2018-10-29 at 15.52.29.png)

   The RTT of gbn is better than ss. Because go back n send multiple packets at a time. So the round trip time between very far distance gbn is better.


3. Write a few simple sentences to describe your conclusion of the comparison
   - To the same protocol it selt, during the increasing of error rates, the send time also increase. When it comes to different protocols, since the go back n sends multiple packets, there is a trade off of this two protocols. When the error rate increasing, sender need to resend packet. Stop and wait resend one packet at a time, go back n resends multiple packets at a time. So there is not very much difference between this two. I believe if the error rate keeps rising, the go back n would be much more worse than stop and wait. Because it needs to resent multiple packets at a time while ss only need to resend one.
   - When it comes to RTT, go back n performs better than stop and wait. Because go back n send multiple packets at a time and it's more efficient. Because stop and wait sends one packet at a time and it takes more times of sending. 
   - Overall go back n performs better than stop and wait.



