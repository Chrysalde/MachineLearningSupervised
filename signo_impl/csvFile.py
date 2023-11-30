# This file is not a main script
if __name__ == '__main__':
    print("[signo:csvFile] -- Error --")
    exit(1)

from typing import TextIO
from signo_impl.SeekingPosition import SeekingPosition

class csvFile:
    r"""Represents a .csv file and provides methods to interact with it.
    
    Attributes
    ----------
        sep: str
            The separator used to fragment the data.

        filepath: str
            The path to the file.

    Internals
    ---------
        __file__: TextIO
            The file object used to interact with the file on the disk.

        __read__: bool
            Specifies whether the object has reading rights.

        __write__: bool
            Specifies whether the object has writing rights.

    Methods
    -------
        truncate\
        truncateline
        parse_column
        seek
        readfile
        readline
        readcolumn
        append
        appendline
        write
        writeline
        count
        at
    """
    __file__:   TextIO
    __read__:   bool
    __write__:  bool

    sep:        str
    filepath:   str

    def __init__(
            self,
            filepath: str,
            /, *,
            sep: str = ';',
            read: bool = True,
            write: bool = True,
            truncate: bool = False,
            append: bool = False
        ) -> None:
        r"""Creates a new signo.csvFile.

        Parameters
        ----------
            filepath: str
                The path leading to the file to use.

            sep: str = ';'
                The separator character(s). Traditionally `;` or `,`, but supports any character.

            read: bool = True
                Specifies whether the object gets reading rights on the provided file.
                Setting this to `False` restricts the amount of actions available.

            write: bool = True
                Specifies wheter the object gets writing rights on the provided file.
                Setting this to `False` restricts the amount of actions available.
                    NOTE: If the file does not exist and `write` is set to true, a new file will be created.

            truncate: bool = False
                Truncates the file, thus removing all data stored within.
                Requires `write` to be `True` to operate, ignored otherwise.

            append: bool = False
                Sets the cursor at the end of the file, traditionally used to add data at the file's end.

        Raises
        ------
            InsufficientPermissionsException
                Raised whenever the object does not have either reading or writing rights over the file.
        """

        self.filepath = filepath
        self.sep = sep
        self.__read__ = read
        self.__write__ = write

        if not self.__read__ and not self.__write__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException

        from os.path import exists
        if write and not exists(self.filepath):
            open(
                file = self.filepath,
                mode = 'x'
            ).close()

        self.__file__ = open(
            file = self.filepath,
            mode = 'r+' if read and write else ('r' if read else '') + ('a' if write else '')
        )

        if self.__write__ and truncate:
            self.truncate()

        self.seek(0, SeekingPosition.FileStart if not append else SeekingPosition.FileEnd)

    def __del__(
            self,
            /
        ) -> None:
        r"""Closes the file"""
        self.__file__.close()

    def truncate(
            self,
            size: int | None = None,
            /
        ) -> None:
        r"""Truncates the file, thus removing all data.

        Parameters
        ----------
            size: int | None = None
                The maximum size of the file. When specified, truncates the fata leaving exactly `size` bytes in total.

        Raises
        ------
            InsufficientPermissionsException
                Raised whenever the object does not have writing rights over the file.
        """
        if not self.__write__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException
        self.__file__.truncate(size)

    def seek(
            self,
            offset: int,
            start_position: SeekingPosition = SeekingPosition.FileStart,
            /
        ) -> int:
        r"""Moves the read/write cursor within the file.

        Parameters
        ----------
            offset: int
                The position to move the cursor to.

            start_position: SeekingPosition = SeekingPosition.FileStart
                The position to start from for positioning the cursor.

        Returns
        -------
            The cursor's new position within the file.
        """
        return self.__file__.seek(offset, int(start_position))

    def truncateline(
            self,
            line_to_remove: int,
            /
        ) -> None:
        r"""Removes a line from the file.

        Parameters
        ----------
            line_to_remove: int
                The index of the line to remove relative to the begining of the file.

        Raises
        ------
            InsufficientPermissionsException
                Raised whenever the object does not have writing rights over the file.
        """
        if not self.__read__ and not self.__write__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException
        wp: int = self.seek(0, SeekingPosition.FileStart)
        rp: int = 0

        line = self.__file__.readline()
        while rp != self.seek(0, SeekingPosition.FileEnd):
            tow = line
            print(f"before read: {rp}")
            self.seek(rp, SeekingPosition.FileStart)
            line = self.__file__.readline()
            rp = self.seek(0, SeekingPosition.CurrentPosition)
            print(f"after  read: {rp}")
            if line_to_remove != 0:
                print(f"before write: {wp}")
                self.seek(wp, SeekingPosition.FileStart)
                self.__file__.write(tow)
                wp = self.seek(0, SeekingPosition.CurrentPosition)
                print(f"after  write: {wp}")
            else:
                print(f"-----------------------")
            line_to_remove -= 1

        self.truncate(wp)

    def appendline(
            self,
            line: list[str | int | float],
            /
        ) -> None:
        r"""Adds a new line at the end of the file.

        Parameters
        ----------
            line: list[str | int | float]
                A list containing the data to write.
        """
        if not self.__write__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException
        self.seek(0, SeekingPosition.FileEnd)
        self.writeline(line)

    def append(
            self,
            data: list[list[str | int | float]],
            /
        ) -> None:
        r"""Adds new lines at the end of the file.

        Parameters
        ----------
            data: list[list[str | int | float]]
                A list of lines to add to the file.
        """
        if not self.__write__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException
        self.seek(0, SeekingPosition.FileEnd)
        for line in data:
            self.writeline(line)

    def writeline(
            self,
            line: list[str | int | float],
            /
        ) -> None:
        r"""Writes a new line at the current position.

        Parameters
        ----------
            line: list[str | int | float]
                A list containing the data to write.
        """
        if not self.__write__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException
        for i, elem in enumerate(line):
            if (i == len(line) - 1):
                from os import linesep
                self.__file__.write(f"{elem}{linesep}")
            else:
                self.__file__.write(f"{elem}{self.sep}")

    def write(
            self,
            data: list[list[str | int | float]],
            /
        ) -> None:
        r"""Writes new lines at the current position.

        Parameters
        ----------
            data: list[list[str | int | float]]
                A list of lines to add to the file.
        """
        if not self.__write__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException
        for line in data:
            self.writeline(line)

    def parse_columns(
            self,
            row: str,
            /
        ) -> list[str | int | float]:
        res: list[str] = []
        for r in row.split(self.sep):
            from signo_impl.utilities import parse_type
            res.append(parse_type(r.strip()))
        return res

    def readfile(
            self,
            /
        ) -> list[list[str | int | float]]:
        if not self.__read__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException
        self.seek(0, SeekingPosition.FileStart)
        data: list[list[str | int | float]] = []
        for line in self.__file__:
            data.append(self.parse_columns(line))
        return data

    def readline(
            self,
            /, *,
            index: int = -1
        ) -> list[str | int | float] | None:
        if not self.__read__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException
        if index < 0:
            line = self.__file__.readline()
            return self.parse_columns(line) if line else None
        else:
            self.seek(0, SeekingPosition.FileStart)
            line = self.__file__.readline()
            while line and index > 0:
                index -= 1
                line = self.__file__.readline()
            return self.parse_columns(line) if line else None

    def readcolumn(
            self,
            index: int,
            /
        ) -> list[str | int | float | None]:
        if not self.__read__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException
        if index < 0:
            from signo_impl.errors import InvalidIndexException
            raise InvalidIndexException
        self.seek(0, SeekingPosition.FileStart)
        col: list[str | int | float | None] = []
        for line in self.__file__:
            cols = self.parse_columns(line)
            if len(cols) > index:
                col.append(cols[index])
            else:
                col.append(None)
        return col

    def count(
            self,
            /, *,
            #values: list[str | int | float],
            row: int = -1,
            column: int = -1
        ) -> dict:
        r"""Counts the occurences of each value within the file.

        Parameters
        ----------
            row: int = -1
                The line to count on.

            column: int -1
                The column to count on.

        Returns
        -------
            A dictionnary with keys being the values present in the file and their associated number of occurences as values.
        """
        line: list[str | int | float | None] | None
        res: dict = {}
        if row >= 0 and column >= 0:
            from signo_impl.errors import MutuallyExclusiveParamtersException
            raise MutuallyExclusiveParamtersException
        if row < 0 and column < 0:
            line = self.readline()
            while line is not None:
                for elem in line:
                    if elem is None:
                        continue
                    if elem in res.keys():
                        res[elem] += 1
                    else:
                        res[elem] = 1
                line = self.readline()
            return res
        elif column >= 0:
            line = self.readcolumn(column)
        else:
            line = self.readline(index=row)
        for elem in line:
            if elem is None:
                continue
            if elem in res.keys():
                res[elem] += 1
            else:
                res[elem] = 1
        return res

    def at(
            self,
            row: int,
            column: int,
            /
        ) -> str | int | float | None:
        r"""Returns the element at the given position.

        Parameters
        ----------
            row: int
                The line (Y) coordinate.

            column: int
                The column (X) coordinate.
        """
        if not self.__read__:
            from signo_impl.errors import InsufficientPermissionsException
            raise InsufficientPermissionsException
        if row < 0 or column < 0:
            from signo_impl.errors import InvalidIndexException
            raise InvalidIndexException
        self.seek(0, SeekingPosition.FileStart)
        line = self.__file__.readline()
        while row > 0:
            self.__file__.readline()
            row -= 1
        if line:
            cols = self.parse_columns(line)
            if len(cols) > column:
                return cols[column]
        return None