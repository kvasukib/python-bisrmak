#!/usr/bin/perl

use strict;
use warnings;
use JSON::XS;
use Net::Patricia;
use Data::Dumper;
use Getopt::Std;
use DBI;
use DateTime;

if(scalar(@ARGV) < 3)
{
    print STDERR "usage: create_ts_triplets.pl mon lnkfn months\n";
    exit -1;
}

my ($mon, $ipfn, @dbs) = @ARGV;

my %ips;
open(IPS, $ipfn)  || die ("could not open ip file\n");
while (<IPS>)
  {
    chomp;
    my @lf = split;
    $ips{$lf[0]}=1;
  }
close(IPS);

my $driver = "SQLite";
my $userid = "";
my $password = "";

foreach my $db_ts (@dbs)
  {
    print STDERR "yyyymm $db_ts\n";
    my $sampfn = "/project/comcast-ping/TSP/adaptive/mon_data/$mon/tsp-samples/$mon.$db_ts.samples.mjl.db";
    next if (! -e $sampfn);

    my $dsn_samp = "DBI:$driver:dbname=$sampfn";
    my $dbh_samp = DBI->connect($dsn_samp, $userid, $password, { RaiseError => 1 }) or die $DBI::errstr;
    print STDERR "Opened samples database successfully\n";
    
    my %ip2id;
    my %id2ip;
    my $samp_ip_sel = $dbh_samp->prepare("select * from ips");
    $samp_ip_sel->execute();
    while (my @row=$samp_ip_sel->fetchrow_array())
      {
	$ip2id{$row[1]}=$row[0];
	$id2ip{$row[0]}=$row[1];
      }
    
    my ($src_ip,$dst_ip);
    my $samp_sel = $dbh_samp->prepare("select src_id, dst_id, ts, round_ts, rtt from samples");
    $samp_sel->execute();
    while (my @row=$samp_sel->fetchrow_array())
      {
	if ( defined $row[0] && defined $row[1] && defined $src_ip  ) {
		$src_ip = $id2ip{$row[0]};
		$dst_ip = $id2ip{$row[1]};
		next if (! defined $ips{$src_ip});
		
		print $row[2]." ".$row[3]." $src_ip $dst_ip ".$row[4]."\n";
		#$rtt{$src_ip}{$dst_ip}{$row[2]}=$row[3]/10;
		#$n_samples{$src_ip}{$dst_ip}++;
		#$timestamps{$row[2]}=1;
	}
      }
  }
