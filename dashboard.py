import pandas as pd


def getvaluecounts(df):
    """
    Returns the frequency count of each unique subject in the 'subject' column of the DataFrame.

    Parameters:
    - df (DataFrame): The DataFrame containing course data with a 'subject' column.

    Returns:
    - dict: A dictionary with subjects as keys and their respective counts as values.
    """
    
    # Using value_counts to count occurrences of each subject and converting the result to a dictionary
    return dict(df['subject'].value_counts())



def getlevelcount(df):
    """
    Returns the number of courses available for each level, based on the 'level' column.
    Skips the first entry in the result (possibly to ignore null or undesired level).

    Parameters:
    - df (DataFrame): The DataFrame containing course data with 'level' and 'num_subscribers' columns.

    Returns:
    - dict: A dictionary where keys are course levels and values are the count of courses per level,
            excluding the first entry.
    """

    # Grouping the DataFrame by 'level' and counting the number of courses (non-null rows in 'num_subscribers')
    level_counts = df.groupby(['level'])['num_subscribers'].count()

    # Converting the Series to a list of (level, count) tuples and skipping the first item
    level_counts_filtered = list(level_counts.items())[1:]

    # Converting the filtered list of tuples to a dictionary and returning
    return dict(level_counts_filtered)



def getsubjectsperlevel(df):
    """
    Creates a dictionary representing the count of each (subject, level) combination.
    The keys are formatted as 'subject_level' strings, and the values are their corresponding counts.

    Parameters:
    - df (DataFrame): The DataFrame containing 'subject' and 'level' columns.

    Returns:
    - dict: A dictionary where each key is in the format 'subject_level' and the value is the count.
    """

    # Grouping the DataFrame by 'subject' and counting occurrences of each 'level' within each subject
    grouped_counts = dict(df.groupby(['subject'])['level'].value_counts())

    # Extracting keys from the grouped result which are tuples like ('subject', 'level')
    ans = list(grouped_counts.keys())

    # Creating labels in the format 'subject_level' by combining each subject and its level
    alllabels = [f"{subject}_{level}" for subject, level in ans]

    # Getting the corresponding count values
    ansvalues = list(grouped_counts.values())

    # Zipping labels and counts into a dictionary
    completedict = dict(zip(alllabels, ansvalues))

    return completedict



def yearwiseprofit(df):
    """
    Processes the course DataFrame to compute:
    - Total profit and number of subscribers year-wise
    - Total profit and number of subscribers month-wise

    Parameters:
    - df (DataFrame): The DataFrame containing course information, including 'price', 'num_subscribers',
                      and 'published_timestamp'.

    Returns:
    - profitmap (dict): Year-wise total profit.
    - subscribersmap (dict): Year-wise total subscribers.
    - profitmonthwise (dict): Month-wise total profit (by month name).
    - monthwisesub (dict): Month-wise total subscribers (by month name).
    """

    # Replacing 'TRUE' and 'Free' strings in the 'price' column with '0'
    df['price'] = df['price'].astype(str).str.replace('TRUE|Free', '0', regex=True)

    # Converting 'price' column to float for numerical operations
    df['price'] = df['price'].astype('float')

    # Calculating profit as product of price and number of subscribers
    df['profit'] = df['price'] * df['num_subscribers']

    # Extracting only the date part from the 'published_timestamp'
    df['published_date'] = df['published_timestamp'].apply(lambda x: x.split('T')[0])

    # Removing a problematic record with invalid date format ('3 hours')
    df = df[df['published_timestamp'].str.contains(r'\d{4}-\d{2}-\d{2}')]
    df = df.drop(df.index[2066])

    # Converting 'published_date' string to actual datetime object
    df['published_date'] = pd.to_datetime(df['published_date'], format="%Y-%m-%d")

    # Extracting year, month, and day from the published date
    df['Year'] = df['published_date'].dt.year
    df['Month'] = df['published_date'].dt.month
    df['Day'] = df['published_date'].dt.day
    df['Month_name'] = df['published_date'].dt.month_name()

    # Aggregating profit and subscriber data year-wise
    profitmap = dict(df.groupby('Year')['profit'].sum())
    subscribersmap = dict(df.groupby('Year')['num_subscribers'].sum())

    # Aggregating profit and subscriber data month-wise (by month name)
    profitmonthwise = dict(df.groupby('Month_name')['profit'].sum())
    monthwisesub = dict(df.groupby('Month_name')['num_subscribers'].sum())

    return profitmap, subscribersmap, profitmonthwise, monthwisesub

