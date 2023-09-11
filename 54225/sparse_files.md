# Sparse Files

## References

- [Arch Linux Refernce: Sparse File](https://wiki.archlinux.org/title/sparse_file)
- [Wikipedia: Sparse File](https://en.wikipedia.org/wiki/Sparse_file)

## Short Short Summary

A sparse file is a file which is partially empty. Some metadate is written
representing the empty data instead of using actual space on the disk (which
saves some disk space).

Sparse files are commonly used as:

- disk images
- database snapshots
- log files

I'm sure there are other uses

## Creating a Sparse File

Using `truncate`:

``` bash
> truncate -s 512M file.img
```

Using `dd`:

``` bash
> dd if=/dev/zero of=file.img bs=1 count=0 seek=512M
```

To tell a file is sparse, you have to look at its actual size and its _apparent_
size:

``` bash
> du -h --apparent-size file.img
512M file.img
> du -h file.image
0    file.img
```

## Convert a normal file to a Sparse file

``` bash
> fallocate -d copy.img
> du -h copy.img
0
```

## Convert a Sparse file to a normal file

``` bash
> cp file.img copy.img --sparse=never
> du -h copy.img
512M
```

## Copy a sparse file

``` bash
> cp --sparse=always new_file.img recovered_file.img
```

## Detecting Sparse Files

If a file's size is greated than the allocated size in the first column, a file
is sparse

``` bash
> ls -ls sparse-file.bin
```

## Sparse files in Python

``` python
>>> with open("myfile.img", 'ab') as sparse:
...     sparse.truncate(10240000)
...
>>> os.stat('myfile.img').st_size
10240000
>>> os.stat('myfile.img').st_blocks*512
0
```
