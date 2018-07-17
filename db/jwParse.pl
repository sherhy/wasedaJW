use strict;
open my $sils, "< output.html" or die "couldn't open output.html";
open my $keys, "> keys.txt" or die "couldn't create keys.txt";
my (
	@keys,
	@tokens,
);

while (my $line = <$sils>) {
	chomp ($line);
	if ($line =~ m/^<td><a href=\"#\" onclick=\"post_submit\(\'JAA104DtlSubCon\'/) {
		@tokens = split(/\'/, $line);
		print $keys "@tokens[3]\n";
	}
}