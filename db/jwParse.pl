use strict;

open my $sils, "< db/output.html" or die "couldn't open output.html";
open my $keys, "> db/keys.csv" or die "couldn't create keys.csv";
my (
	@keys,
	@tokens,
);


while (my $line = <$sils>) {
	chomp ($line);
	if ($line =~ m/^<td><a href=\"#\" onclick=\"post_submit\(\'JAA104DtlSubCon\'/) {
		@tokens = split(/\'/, $line);
		print $keys "@tokens[3], ";
	}
}
close $keys or die "couldn't close keys.csv";