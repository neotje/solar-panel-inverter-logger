#!/usr/bin/perl -w

use POSIX qw(strftime mktime);
use Time::HiRes qw(time sleep);
use LWP::UserAgent;
use HTTP::Request::Common;
use Device::SerialPort qw (:STAT);
use Switch;

use lib qw(./lib);

use DeviceCMS2000;
use CMS2000emul;
use strict;
use warnings;

my $command = $ARGV[0];
my $serialnumber = "test";

switch($command) {
    case "get" {
        my $port = $ARGV[1];
        my $link;

        #$link = new CMS2000emul;
        $link = new Device::SerialPort($port) || die "new: $!\n";
        $link->error_msg(1);		# use built-in hardware error messages
        $link->user_msg(1);		# use built-in function messages
        $link->can_ioctl()		|| die "Has no ioctl\n";
        $link->baudrate(9600)	|| die 'fail setting baudrate, try -b option';
        $link->parity("none")	|| die 'fail setting parity';
        $link->databits(8)		|| die 'fail setting databits';
        $link->stopbits(1)		|| die 'fail setting stopbits';
        $link->handshake('none')	|| die 'fail setting handshake';
        $link->datatype('raw')	|| die 'fail setting datatype';
        $link->write_settings		|| die 'could not write settings';
        $link->read_char_time(0);	# don't wait for each character
        $link->read_const_time(480);	# 512*9/9600 second per unfulfilled "read" call
        $link->dtr_active(0);		# set power to +++
        $link->rts_active(1);		# set power to ---

        my $device = new DeviceCMS2000(link => $link, serialnumber => $serialnumber);

        my $data = $device->Status;

        print("serial|", join('|', $data->select(undef, 'key')), "\n");
        print($device->{serialnumber}, "|", join('|', $data->select), "\n");
    }
}